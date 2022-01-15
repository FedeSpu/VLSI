- converter.py: this program converts the txt instances from instancesTXT in dzn files in instancesDzn. 
		An order can be imposed through the boolelan variables 
		WIDTH_DEC_ORDER, HEIGHT_DEC_ORDER and AREA_DEC_ORDER

- runner.py: automatically executes minizinc model over dzn instances from directories instancesDzn.
	     Directory of instances can be changed in dir_instance. The model (chuffed or gecode) can be
 	     changed in model_name and the solver can be changed in solver_name. solver_name and model must
	     be the same (chuffed or gecode)

- printBlocks.py: plot the rectangles with the found coordinates. The instance printed can be changed in file_name
