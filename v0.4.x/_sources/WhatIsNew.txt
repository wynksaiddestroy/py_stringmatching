What is New? 
============

Compared to Version 0.3.0, the following are new:

  * Five similarity measures written in Python have been Cythonized to run much faster. These are Affine, Jaro, Jaro Winkler, Needleman Wunsch, and Smith Waterman. 

  * We have also empirically evaluated the runtime of Jaccard (written in Python) and found that it is already very fast. Thus, Cythonizing it is unlikely to yield much of a speedup.

  * Note that in Version 0.3.x (and earlier versions), edit distance has been Cythonized. Thus, the set of all Cythonized similarity measures consists of edit distance, Affine, Jaro, Jaro Winkler, Needleman Wunsch, and Smith Waterman.

  * In subsequent versions, it would be highly desirable to Cythonize remaining similarity measures, including Dice, cosine, etc.

  * For this package, we add a runtime benchmark (consisting of several datasets and scripts) to measure the runtime performance of similarity measures. This benchmark can be used by users to judge whether similarity measures are fast enough for their purposes, and used by developers to speed up the measures. 
