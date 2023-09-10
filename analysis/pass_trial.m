function pass = pass_trial(avgs, stds, jsonStr, significance, count_threshold)
    % we optimize the significance and count_threshold - these are our
    % hyperparameters
    % significance = 0.0550;
    % count_threshold = 9;

    % jsonStr = fileread('sample.txt');
    jsonTrial = jsondecode(jsonStr);
    vals = params_for_trial(jsonTrial);
    
    % we keep track of the amount of successful tests, where Ha is not
    % accepted
    successful = 0;
    for idx = 1:numel(avgs)
        % we calculate the z score
        % avgs{1, idx}
        % stds{1, idx}
        
        if isnan(vals(1, idx))
            continue
        end

        z_score = (vals(1, idx) - avgs{1, idx}) / stds{1, idx};
        % then we calculate the percentile of the z score
        probability = normcdf(z_score);
        % finally we see if the z score is statistically significant based
        % on our threshold
        if (probability <= 1 - (significance / 2)) && (probability >= significance / 2)
            successful = successful + 1;
        end
    end
    
    % we ensure that the count_threshold is low-high enough for
    % accuracy-recall
    if successful >= count_threshold
        pass = 1;
    else 
        pass = 0;
    end
end
