% trying out some different viz of the 2048-dim that inception gives back
load('inception.mat');

[N,n] = size(matrix);

no_dims = round(intrinsic_dim(matrix, 'MLE'));
disp(['MLE estimate of intrinsic dimensionality: ' num2str(no_dims)]);

% WOW--MLE says it's 13 dims; best results from PCA on first 2 and then
% laplacian eigenmaps!!!!!!!! (it preserves all data points)
[mappedX, mapping] = compute_mapping(matrix, 'PCA', no_dims);	
figure, scatter3(mappedX(:,1), mappedX(:,2), mappedX(:,3)); title('Result of PCA (3 components)');

[mappedX, mapping] = compute_mapping(matrix, 'Laplacian', no_dims, 7);	
figure, scatter3(mappedX(:,1), mappedX(:,2), mappedX(:,3)); title('Result of Laplacian Eigenmaps'); drawnow
size(mappedX)
size(mapping)

% Now cluster this!
X = mappedX(:,1:3);
eucD = pdist2(X,X);
clustTreeEuc = linkage(eucD,'average');
cophenet(clustTreeEuc,eucD)

[h,nodes] = dendrogram(clustTreeEuc,0);
h_gca = gca;
h_gca.TickDir = 'out';
h_gca.TickLength = [.002 0];
h_gca.XTickLabel = [];


% https://www.mathworks.com/help/stats/examples/cluster-analysis.html
hidx = cluster(clustTreeEuc,'criterion','distance','cutoff',0.19);
for i = 1:13
    clust = find(hidx==i);
    clust
    scatter3(X(clust,1),X(clust,2),X(clust,3));
    hold on
end
hold off
grid on

%[mappedX, mapping] = compute_mapping(matrix, 'DiffusionMaps', no_dims);	
%figure, scatter(mappedX(:,1), mappedX(:,2)); title('This is the testing one'); drawnow