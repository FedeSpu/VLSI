include "globals.mzn";
include "fzn_diffn.mzn";
include "fzn_diffn_reif.mzn";
include "lex_lesseq.mzn";
include "lex_greater.mzn";

% Variables instantiation
int: n_blocks;                       
set of int: BLOCKS = 1..n_blocks;    
array[BLOCKS] of int: height;        

int: max_width;                      
array[BLOCKS] of int: width;         

int: h = sum(height);
int: w = sum(width);                  
array[BLOCKS] of var 0..h: cornery;  
array[BLOCKS] of var 0..w: cornerx;

% Lower bound of makespan
var int: makespan = max(b in BLOCKS)(cornery[b] + height[b]);

var int: min_reach_h = ceil((sum(b in BLOCKS)(width[b] * height[b]) div max_width));

constraint makespan >= max(min_reach_h,max(height));


constraint forall(b in BLOCKS) (
  cornerx[b] + width[b] <= max_width /\
  cornery[b] + height[b] <= makespan
);

% Global constraints
constraint cumulative(cornery, height, width, max_width);

constraint cumulative(cornerx, width, height,max(min_reach_h,max(height))); %makespan 

constraint diffn(cornerx, cornery, width, height);

% Width of blocks > max_width / 2
array[BLOCKS] of var bool: R;

constraint forall(b in BLOCKS)(R[b]<-> width[b] > max_width / 2);

constraint forall(b in BLOCKS)(
  if R[b]
  then cornerx[b] = 0
  endif
);

% Symmetry breaking constraints
constraint forall(r1,r2 in BLOCKS where r1 < r2 /\ width[r1]=width[r2] /\ height[r1]=height[r2]) (lex_less([cornerx[r1],cornery[r1]],[cornerx[r2],cornery[r2]]));  

constraint forall(r1,r2 in BLOCKS where r1 < r2 /\ cornery[r1]=cornery[r2] /\ cornerx[r1]+width[r1]=cornerx[r2] /\ height[r1]=height[r2]) 
(lex_less([cornerx[r1]],[cornerx[r2]])); 

constraint forall(r1,r2 in BLOCKS  where r1 < r2 /\ cornerx[r1]=cornerx[r2] /\ cornery[r1]+height[r1]=cornery[r2] /\ width[r1]=width[r2]) 
(lex_less([cornery[r1]],[cornery[r2]]));

% Search strategies 
%first strategy           
%solve minimize makespan;

%second strategy  
/*
solve :: seq_search([int_search([makespan], smallest, indomain_min),
                 int_search(cornery, input_order, indomain_min)
                 ]) minimize makespan;
*/

%third strategy
solve :: seq_search([int_search([makespan], smallest, indomain_min),
                 int_search(cornerx, input_order, indomain_min)
                 ]) minimize makespan;       


output["\(max_width) \(makespan)\n\(n_blocks)\n"] ++
  ["\(width[b]) \(height[b]) \(cornerx[b]) \(cornery[b])\n" | b in BLOCKS];