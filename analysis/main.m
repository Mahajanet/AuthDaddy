function weights = main(jsonName)
    % jsonStr = fileread('leokeystrokes.txt');
    jsonStr = fileread(jsonName);
    jsonData = jsondecode(jsonStr);
    % JSON code is generated when the user fills the password fields
    % JS sends JSON to this matlab script

    jsonData

    if isstruct(jsonData) && ~iscell(jsonData)
        jsonData = struct2cell(jsonData);
    end
    
    
    % constants for the number of variables and trials
    NVARS = 9;
    NTRIALS = 10;
    
    % we prepopulate a table with zeros
    % it has each of the variables and mean/std dev associated
    % with the vars
    % aux = zeros(NVARS, NTRIALS);
    variableNames = {'avgPress', 'avgJump', 'stdPress', 'stdJump', 'nBack', ...
                    'longPress', 'shortPress', 'longJump', 'shortJump'};
    userProfile = table('Size', [NTRIALS, NVARS], 'VariableTypes', ...
        repmat({'double'}, 1, NVARS), 'VariableNames', variableNames);
    
    % iterate through each list
    for rowIdx = 1:NTRIALS
        currList = jsonData(rowIdx, :);
        currList = currList{1, 1};
        currList = currList';
        currList
        % check if current list is a cell array (containing dict)
        if isstruct(currList)
            result = params_for_trial(currList);

            % check if result is valid size
            if isequal(size(result), [1, NVARS])
                userProfile(rowIdx, :) = num2cell(result);
            end
        end
    end
    
    % avgs and stds are saved for future use
    avgs = mean(userProfile, 1);
    stds = std(userProfile, 0);
    
    weights = [avgs;stds];
end