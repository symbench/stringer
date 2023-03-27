generate_string(Z) :- string_generator(Z, 0, 2, 3).

string_generator(Clusters,Counter, ClusterCount, ClusterSize) :- Counter = 0, 
    generate_fuselage_cluster(NewCluster, ClusterSize), append([], NewCluster, IntermediateClusters), 
    NewCounter is (Counter + 1), string_generator(Clusters, IntermediateClusters, NewCounter, ClusterCount, ClusterSize).

string_generator(Clusters, PreviousClusters, Counter, ClusterCount, ClusterSize) :- Counter > 0, Counter < ClusterCount, 
    generate_cluster(NewCluster, ClusterSize), append(PreviousClusters, NewCluster, IntermediateClusters), 
    NewCounter is Counter + 1, string_generator(Clusters, IntermediateClusters, NewCounter, ClusterCount, ClusterSize).

string_generator(Clusters, PreviousClusters, Counter, ClusterCount, ClusterSize) :- 
    Counter = ClusterCount, generate_cluster(NewCluster, ClusterSize), append(PreviousClusters, NewCluster, Clusters).

generate_fuselage_cluster(ReturnCluster, ClusterSize):- append([], ['[', 'f'], ClusterStart), 
    fill_cluster(ClusterStart, OpenCluster, ClusterSize), append(OpenCluster,[']'], ReturnCluster).

generate_cluster(ReturnCluster, ClusterSize) :- append([], ['['], ClusterStart), fill_cluster(ClusterStart, OpenCluster, ClusterSize), 
                          append(OpenCluster,[']'], ReturnCluster). 

% Standard fill, recursing
fill_cluster(OldTokens,ReturnTokens, ClusterSize) :- length(OldTokens, ListLength), ListLength < ClusterSize, 
    prop_tokens(NewToken), append(OldTokens, NewToken, IntermediateTokens), fill_cluster(IntermediateTokens, ReturnTokens, ClusterSize).

% Wing cluster
fill_cluster(OldTokens,ReturnTokens, ClusterSize) :- length(OldTokens, ListLength), ListLength < 2, 
    wing_token(NewToken), append(OldTokens, NewToken, ReturnTokens).

% Subcluster
fill_cluster(OldTokens,ReturnTokens, ClusterSize) :- length(OldTokens, ListLength),
    ListLength < ClusterSize, 
    SubclusterSizeMax is ClusterSize - ListLength + 1, random(1, SubclusterSizeMax, SubclusterSize),
    append(OldTokens, ['('], SubclusterStart), SubclusterOffset is ListLength, 
    fill_subcluster(SubclusterStart, SubclusterReturn, SubclusterSize, SubclusterOffset),
	append(SubclusterReturn, [')'], IntermediateTokens), NewClusterSize is ClusterSize + 2, 
    fill_cluster(IntermediateTokens, ReturnTokens, NewClusterSize).

% Return case
fill_cluster(OldTokens,ReturnTokens, ClusterSize) :- length(OldTokens, ListLength), ListLength >= ClusterSize, 
    prop_tokens(NewToken), append(OldTokens, NewToken, ReturnTokens).

% Subcluster recursive case
fill_subcluster(OldTokens,ReturnTokens, ClusterSize, SubclusterOffset) :- length(OldTokens, ListLength), SubclusterLength is ListLength - SubclusterOffset, 
    SubclusterLength < ClusterSize, prop_tokens(NewToken), append(OldTokens, NewToken, IntermediateTokens), 
    fill_subcluster(IntermediateTokens, ReturnTokens, ClusterSize, SubclusterOffset).

% Subcluster return case
fill_subcluster(OldTokens,ReturnTokens, ClusterSize, SubclusterOffset) :- length(OldTokens, ListLength), SubclusterLength is ListLength - SubclusterOffset, 
    SubclusterLength >= ClusterSize, prop_tokens(NewToken), append(OldTokens, NewToken, ReturnTokens). 

prop_tokens([p]).
prop_tokens([h]).
prop_tokens([l]).
wing_token([w]).