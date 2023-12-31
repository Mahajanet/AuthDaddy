sigvalues = linspace(.005,.15,30);
kvalues = [5 6 7 8 9];
people = ["jvm" "leo" "marko" "mike"];

recall_arr = [];
precision_arr = [];
p_arr = [];
most_precise = 0

for p_idx = 1:numel(sigvalues)
    sigvalue = sigvalues(p_idx);
    for k_idx = 1:numel(kvalues)
        p_arr = [p_arr, p_idx];

        kvalue = kvalues(k_idx);
        model_cm = [0 0;0 0];
        for pers_idx = 1:numel(people)
            name = people(pers_idx);
            % instantiate model
            fStr = sprintf('../testdata/%s_%s_1.txt',name, name);
            % get avgs and stds
            weights = main(fStr);
            avgs = weights(1,:);
            stds = weights(2,:);
            
            cm = compute_conf(name, avgs, stds, sigvalue, kvalue, people);
            model_cm = model_cm + cm;
        end
        % recall - you want to catch them all
        recall = model_cm(2,2) / (model_cm(2,1) + model_cm(2,2));
        recall_arr = [recall_arr, recall];

        % precision - make a careful decision
        precision = model_cm(2,2) / (model_cm(1,2) + model_cm(2,2));
        precision_arr = [precision_arr, precision];

        if recall >= 0.30 && precision > most_precise
            most_precise = precision;
            % 0.1450, 9 has best precision within recall
            % 0.0550, 9 has good recall (50%) and very precise
        end
    end
end

size(recall_arr)
size(precision_arr)

figure;
plot(p_arr,recall_arr,'-o','DisplayName','Recall','LineWidth',1.5);
hold on;

plot(p_arr,precision_arr,'-s','DisplayName','Precision','LineWidth',1.5);

xlabel('p');
ylabel('Percentage');
legend('Location', 'Best');
title('Recall and Precision vs. p');
grid on;

hold off;
function conf_matrix = compute_conf(name, avgs, stds, sigvalue, kvalue, people)
    % trials are the json strings for the test data
    % y is 0 or 1, it is the expected outcome
    pred = [];
    exp = [];
    for i = 1:numel(people)
         other = people(i);
         if (name == other)
             for j = 2:4
                 fName = sprintf('../testdata/%s_%s_%d.txt',name, name, j);
                 jsonStr = fileread(fName);
                 jsonData = jsondecode(jsonStr);    
                 for rowIdx = 1:10
                     data = jsonData(rowIdx, :);
                     pred = [pred, (pass_trial(avgs, stds, jsonencode(data), sigvalue, kvalue))];
                     exp = [exp, 1];
                 end
             end
         else
             fName = sprintf('../testdata/%s_%s.txt', other, name);
             jsonStr = fileread(fName);
             jsonData = jsondecode(jsonStr);
             for rowIdx = 1:10
                 data = jsonData(rowIdx, :);
                 pred = [pred, pass_trial(avgs, stds, jsonencode(data), sigvalue, kvalue)];
                 exp = [exp, 0];
             end
         end
    end
    
    conf_matrix = [0 0; 0 0]; % true neg, false pos, false neg, true pos

    for idx = 1:numel(pred)
        conf_matrix(exp(idx)+1, pred(idx) + 1) = ...
            conf_matrix(exp(idx)+1, pred(idx) + 1) + 1;
    end
end