What is New? 
============

Compared to Version 0.1.0, the following are new: 

  * Qgram tokenizers have been modified to take a flag called "padding". If this flag is True (the default), then a prefix and a suffix will be added to the input string before tokenizing (see the Tutorial for a reason for this). 

  * Version 0.1.0 does not handle strings in unicode correctly. Specifically, if an input string contains non-ascii characters, a string similarity measure may interpret the string incorrectly and thus compute an incorrect similarity score. In this version we have fixed the string similarity measures. Specifically, we convert the input strings into unicode before computing similarity measures. NOTE: the tokenizers are still not yet unicode-aware. 

  * In Version 0.1.0, the flag "dampen" for TF/IDF similarity measure has the default value of False. In this version we have modified it to have the default value of True, which is the more common value for this flag in practice. 
