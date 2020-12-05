[~,~,raw1] = xlsread('1') ;
[~,~,raw2] = xlsread('Book1') ;
incorrectIndexes = zeros(size(raw1, 1), 2);%indexes stored in this array. Initialized for faster access/computation
numIncorrect = 0; % stores the count of number of differences encountered
if size(raw1) == size(raw2) % stop execution if unequal size
    indexRows_error = find(all(cellfun(@isequal, raw1.', raw2.')) == 0); % compute index of rows, where there is a mismatch
%     indexCols_error = find(all(cellfun(@isequal, raw1.', raw2.')) == 0); %compute index of cols where there is mimatch
% commented out the above method to showcase both the approaches for matching values. 
% for loop approach
    for indexrow = 1:length(indexRows_error)
        row = indexRows_error(indexrow);
        for col = 1:size(raw1, 2)
            if(string(raw1{row, col}) ~= string(raw2{row, col}))
                numIncorrect = numIncorrect + 1;
                incorrectIndexes(numIncorrect, 1) = row;
                incorrectIndexes(numIncorrect, 2) = col;
            end
        end        
    end
else
    disp("Sizes of files unequal. Exiting");
end