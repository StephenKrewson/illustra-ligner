M = csvread('ID-to-embedding.csv');
[L,delimiter] = importdata('filepath-to-synset.csv');


% https://gist.github.com/maraoz/388eddec39d60c6d52d4

% Truncate data since we are missing a few WordNet labels
M = M(1:size(L,1),:);

% Convert the labels to a histogram based on unique counts--what are most
% popular?
[idx,label,GL] = grp2idx(L);
figure; hist(idx,unique(idx));
set(gca,'xTickLabel',label); title('Most Common WordNet IDs for Newtonian System Images');
xlabel('Label Index (N=59)');ylabel('Count');
print('telescope-histogram.png','-dpng');

% Color the pairwise distances plot by the 59 labels
figure; scatter(M(:,1),M(:,2),80,idx,'filled');
text(M(:,1),M(:,2),L);
title('Distance Matrix for 2-D Embedding of Newtonian System Images');
print('telescope-distances.png','-dpng');

% Get the top 10 wordNet clusters
top = sortrows(tabulate(idx),-2);
label(top(1:10,1))
