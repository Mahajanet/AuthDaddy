function pass = critical_trial(avgs, stds, jsonStr, prob_threshold, count_threshold)

    % jsonStr = fileread('sample.txt');
    jsonTrial = jsondecode(jsonStr);
    vals = params_for_trial;
    
    successful = 0;
    for idx = 1:numel(avgs)
        z_score = (vals(1, idx) - avgs(1, idx)) / stds(1, idx);
        probability = normcdf(z_score);
        if probability >= prob_threshold
            successful.increment()
        end
    end
    
    if successful >= count_threshold
        pass = 1;
    else 
        pass = 0;
    end
end