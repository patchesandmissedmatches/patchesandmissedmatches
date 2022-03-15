# PaReco: Patched Clones and Missed Patches among the Divergent Variants of a Software Family

This is the replication package for the submitted paper. It contains the Python code of our simulation,
the dataset containing all repositories and the code used for analysis.

## Extending ReDeBug
This work reuses the classification method of [`ReDeBug`](https://github.com/dbrumley/redebug). We extend their classification method to not only identify missed security patches, but to also identify missed, duplicated and split cases in any type of patch for the programming languages Java, Python, PHP, Perl, C, shellscript and Ruby.
We also look deeper into a patch and classify each file and each hunk in the .diff for that file.

## Obtaining the artifacts
Clone the repository to a location of your choice using [git](https://git-scm.com/):
  ```
  git clone https://github.com/patchesandmissedmatches/patchesandmissedmatches.git
  ```

## Project structure
Files and folders

* [`Methods`](Methods) contains helper files used in the main files. There are 9 helper files.
    * ['patchExtractionFunctions.py'](Methods/patchExtractionFunctions.py) - It has functions for extracting patches from GitHub
	* [`analysis.py`](Methods/analysis.py) - It is used for plotting the classfication results.
	* [`classifier.py`](Methods/classifier.py) - It contains helper functions used when classifying.
	* [`commitLoader.py`](Methods/) - File with helper functions used on/for commit data
	* [`common.py`](Methods/common.py) - This file is re-used from the original implementation or ReDeBug, also used when classification.
	* [`dataLoader.py`](Methods/dataLoader.py) - Helper file to retreive all PR data
	* [`totals.py`](Methods/totals.py) - Classifies every patch based on the classifications of the files in the patch and calculates totals for each repository pair.
	* [`patchLoader.py`](Methods/patchLoader.py) - This file is re-used from the original implementation or ReDeBug. It is used to load a patch, process it and make it ready for classification.
	* [`sourceLoader.py`](Methods/sourceLoader.py) - This file is re-used from the original implementation or ReDeBug. It is used to load a file, process it and make it ready for classification. 
* [`Empty_files`](Empty_files) contains 7 empty files for each of the 7 programming languages the tool can process. These are used whenever a diff file is needed for an added or removed file in a patch.
* [`Repos_prs`](Repos_prs) will contain the retrieved pull request data.
* [`Repos_files`](Repos_files) will contain the retrieved files from the pull requests per repository pair.
* [`Repos_results`](Repos_results) will contain the classification results for the pull requests per repository pair.
* [`Repos_totals`](Repos_totals) will contain the totals data per repository pair.
* [`src`](src) contains the files that are at the heart of the tool for classification.
* [`tokens.txt`](tokens.txt) contains the GitHub API tokens seperated by only a comma (,)

Create the Repos_prs, Repos_files, Repos_results and Repos_totals directories before running the tool.

## Requirements
The required libraries are: ```re, pickle, argparse, requests, json, numpy, matplotlib, bitarray and python-magic```
Install the required libraries with pip, e.g.:
```
pip install re
```

```libmagic``` package: ```apt-get install libmagic-dev``` on Ubuntu/Debian, ```brew install libmagic``` on OSX

## Running the tool
There are 3 notebooks that are at the heart of this tool: [`getData.ipynb`](src/getData.ipynb), [`classify.ipynb`](src/classify.ipynb) 
and [`analysis.ipynb`](src/analysis.ipynb): getData.ipynb extracts the pull request data from the GitHub api
and stores it in Repos_prs after which classify.ipynb extracts the files from each pull request, the diffs
for each modified/added/removed file and classifies the hunk and files. Then analysis.ipynb does the last classification for the patch
and calcualtes the total classification per repository and plots the results. [`timeLag.ipynb`](src/timeLag.ipynb) calcualtes the techinical lag for each patch.

## Examples
The folder [`Examples`](Examples) contains a Jupyter notebook that can be used to quickly run the tool and classify one or more pull requests for two variant repositories. A simple class [`PaReco`](Examples/PaReco.py) exists that does the classification. Running the notebook for source and target variant mrbrdo/rack-webconsole -> codegram/rack-webconsole and pull request 2 will give an output as:

```
mrbrdo/rack-webconsole -> codegram/rack-webconsole
Pull request nr ==> 2
File classifications ==>
	 lib/rack/webconsole/assets.rb
		 Operation - MODIFIED
		 Class - ED
Patch classification ==> ED
```
Additionally the classification distribution will also be plotted.

To use this notebook for classification, you need to have the source and target repository names, list of pull requests and the cut off date.

Create the Repos_files and Repos_results directories before running the examples.

## GitHub tokens
To access private repositories, and to have a higher rate limit, GitHub tokens are needed.

They can be set in the [tokens.txt](tokens.txt) file or by directly inserting it in the ```token_list``` in the notebooks. GitHub tokens are a must to run the code, because of the high number of requests done to the GitHub API. 
Every token in the tokens.txt file is seperated by only a comma. The user can add as many tokens as needed. A minimal of 5 tokens can be used to safely execute code and to make sure that the rate limit is not reached for a token.

## Repoducing results
Using the [`sorted_all_dataset.pkl`](sorted_all_dataset.pkl) with the notebooks in the [`src`](src) folder, the results presented in the paper can be reproduced.

