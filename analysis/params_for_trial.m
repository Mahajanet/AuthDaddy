function lambdas = params_for_trial(biometrics)

    % we prepopulate arrays for number of total entries,
    % time letters on the keyboard are released
    % time letters on the keyboard are pressed
    numEntries = numel(biometrics);
    timeReleased = zeros(1, numEntries);
    timePressed = zeros(1, numEntries);
    % keys = zeros(1, numEntries);
    backcount = 0;
    sizes = size(biometrics);
    if sizes(1) > 1
        biometrics = biometrics';
    end
    % iterate through the trials
    for idx = 1:numel(biometrics)
        % forward-fill empty values
        if (isempty(biometrics(1, idx).timereleased))
            timeReleased(1, idx) = biometrics(1, idx).timepressed + 100;
        else
            timeReleased(1, idx) = biometrics(1, idx).timereleased;
        end
        timePressed(1, idx) = biometrics(1, idx).timepressed;
        % handle backspace logic early
        if biometrics(1, idx).key == "Backspace"
            backcount = backcount + 1;
        end
    end

    % subtract arrays to get time b/w keys being pressed
    keyPress = timeReleased - timePressed;
    % get difference of timePressed values to get time b/w
    % each key getting pressed
    keyJump = diff(timePressed);

    lambdas = [];

    % avg time per key press
    lambdas = [lambdas, mean(keyPress)];
    
    % avg time between key presses
    if isempty(mean(keyJump))
        lambdas = [lambdas, NaN];
    end
    lambdas = [lambdas, mean(keyJump)];
    
    % std time per key press
    if isempty(std(keyPress))
        lambdas = [lambdas, NaN];
    end
    lambdas = [lambdas, std(keyPress)];
    
    % std time between key presses
    if isempty(std(keyJump))
        lambdas = [lambdas, NaN];
    end
    lambdas = [lambdas, std(keyJump)];
    
    % number of back spaces
    lambdas = [lambdas, backcount];
    
    % longest key press (intra)
    lambdas = [lambdas, max(keyPress)];
    
    % shortest key press
    lambdas = [lambdas, min(keyPress)];
    
    % biggest jump (inter)
    if isempty(max(keyJump))
        lambdas = [lambdas, NaN];
    end
    lambdas = [lambdas, max(keyJump)];
    
    % shortest jump
    if isempty(min(keyJump))
        lambdas = [lambdas, NaN];
    end
    lambdas = [lambdas, min(keyJump)];

end