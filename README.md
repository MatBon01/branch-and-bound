# SRA-CW

The code can be run using the following command with python 3.9:

```bash
python3 branch_and_bound.py
```

This will run the best solution which has been explained in the report and output the final schedule along with the file `bbschedule.log` containing the iteration level output. To change the method use you can change the values of explorer,bounder and brancher in the main function of branch_and_bound to the following:
explorer = JumpTracker() or DepthFirstSearch()
bounder = AllOthersOnTimePolicy()
brancher = AllBranchesPolicy(jobs, bounder) or BeamSearchPolicy(jobs, bounder, lambda level: 2) (where the third argument is the beam width when given a level)