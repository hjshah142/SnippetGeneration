# Snippet Generation for Arguments

## Master Thesis:  Modelling the context and argumentativeness of sentences in argument Snippet Generation 

The thesis work is an extended version of the approach of Alshomary et al. [1] for the snippet generation for arguments.


### Table of Contents


- [Project Overview](#project-overview)
- [Project Setup](#project-setup)
- [References](#references)
- [Evaluation](#evaluation)




## Project Overview

### Task Definition
 **Snippet Generation for the arguments.** The task focuses on automatically generating a snippet for an argument search. Snippets are generated from the argument and contain two sentences extracted from an argument. The definition provided by Alshomary et al. for an [extractive snippet generation for arguments ](https://dl.acm.org/doi/10.1145/3397271.3401186 ) is followed for the generation of a snippet for an argument. Alshomary et al. [1] defined the snippet generation task as :


` "Given a natural language argument, generate a two-sentence snippet that best repre-sents the argument’s main claim and main reason."`
 
## System Architecture
The figure shows the architecture of the extended version of snippet generation (Alshomary et al., 2020). The figure expresses the two main tasks performed  in this snippet generation project:
1. Argument context modelling 
2. Argumentativeness computation


![System Architecture](./data/ThesisArchitecture.svg)


The centrality score is calculated from sentences of an argumentative text. An argumentative text contains a given argument and retrieved arguments. Aspects detection is performed on arguments to retrieve arguments from corpora. Retrieved arguments are added to the context of an argument. The argumentativeness score for a sentence in a given argument is computed using argumentation mining approaches. As shown in the figure, the importance score is the sum of the centrality score and argumentative score. Importance score for sentences for all sentences in the arguments using the variant of  PageRank algorithm Page et al., 1999 [3]. All sentences of arguments are ranked using the importance score, and the two most ranked sentences in their original ordering are selected as the snippet of an argument.


## Project Setup
### Installation and setting up the python environment
The Code is written in Python 3.7. Please ensure that you have the same version of python. Ensure that you have the latest version of pip installed. 

To install the required packages and libraries using _pipenv_ , run this command in the project directory after cloning the repository:

`pip install -r requirements.txt`

To install the required packages and libraries using _condaenv_ , run the command below in the project directory after cloning the repository. This step creates an environment from an environment.yml file

`conda env create -f environment.yml`

### Project Run
After installing the libraries and setting up the python environment for the snippet generation Project, Project can be run using 
1. Python Console: To run snippet generation project from the python console
   * Run `setup.py`
   * Run `__init.py__`
  __init.py__ calls the class `SnippetGenerator` (snippetGenerator.py) to  generate snippets for the arguments 
        
2. Python Notebook (Jupyter Notebook): To run snippet generation project on jupyter notebook
    * Run all the cells of the  [SnippetsGenerationEvaluation_google_colab.ipynb](SnippetsGenerationEvaluation_google_colab.ipynb). 
    
#### To run the project using GoogleColab
Clone the repository in the Google drive and open the notebook file [SnippetsGenerationEvaluation_google_colab.ipynb](SnippetsGenerationEvaluation_google_colab.ipynb) in google colaboratory and run the cell of the .
describes our approaches for argument context modelling and argumentativeness computation. 
    
`SnippetGenerator` class generates the snippet for the arguments in the file  [snippets.txt](data/snippets.txt) and returns generated snippets and the accuracy of the generated snippets. Generated snippets will be saved in the file 
[snippetsGenerated.txt](data/snippetsGenerated.txt) automatically.  Codes for aspects detection on args.me, Argumentative Sentence Classifier and Claim classification model can be found in notebook files [ArgumentAspectsContextDataset.ipynb](ArgumentAspectsContextDataset.ipynb), [Argumentative_Classification(RobertArg).ipynb](Argumentative_Classification(RobertArg).ipynb) and   
[ClaimProbabilityPredictionModel.ipynb](Argumentative_Classification(RobertArg).ipynb) . Due to data privacy and security concerns, args.me aspect dataset  and pre-trained model for the claim classifier model are not uploaded to the Github repository.

Parameters of _SnippetGenerator_ class:

- **arguments**: List of arguments in passed in JSON formats 

- **d**: damping factor value

- **mc_method**: Markov chain methos `['power','eigen','linear','krylov']`

- **aspects_arguments_max**: Maximum number of aspect matching arguments extracted from the argument corpus

- **aspects_weights**:  To set a minimum value for the weight of an aspect in an aspect list while retrieving arguments having the same aspects. 

- **argument_context_matrix**: To select the context of an argument using different approaches . The context of an argument is selected by mapping the respected value of the context to 1.
                            `['query',same page','aspect'] ` default value:`[1, 1, 1]`

- **argumentative_score_method**: Different Approaches  to compute argumentative score  `[claim_discourse_markers, argumentative_score, claim_probability_score, hybrid_approach]`





Different values of this parameter can be passed to evaluate snippet generation using a different configuration.   


## Evaluation
- Measuerd the Accuracy of argument in selecting sentences from the ground-truth snippet
 
 ![image](https://user-images.githubusercontent.com/38283252/146687846-3983c4a4-5b96-4ab5-86b3-d9a5155e7b1c.png)

- Automatic Evaluation performed for three different tasks by changing the value of d in the following equation:

![image](https://user-images.githubusercontent.com/38283252/146687895-a8477809-bffa-409e-991f-a1baeb119349.png)

1. Argument Context Modelling (d = 0)
2. Argumentativeness Computation (d = 1)
3. Topic-wise Snippet Generation Evaluation (0 < d < 1)


### 1. Argument Context Modelling Evaluation(d = 0)

- To Find the optimum value of number of aspect matching arguments
- Argument Context Matrix Set to :  [1, 0, 1]
- M: Most relevant aspect matching arguments
- Gradually increasing the value of M Adding more aspect specific arguments (M) increases the accuracy of the snippets till some threshold value Adding more arguments than the threshold value diminishing the accuracy
![image](https://user-images.githubusercontent.com/38283252/146688252-b3ba7d31-7a3c-465a-b128-5bac34cd066a.png)

- Modelling the context of an argument: Improves the accuracy of the snippet generation leads to 8% Gain then baseline

 ![image](https://user-images.githubusercontent.com/38283252/146688234-d2f9536b-ae3d-4de4-9bce-ba239fc9b7d3.png)
 
### 2. Argumentativeness Computation Evaluation (d = 1)
- Evaluation of all approaches of argumentativeness Computation:
- Claim probability score approach: Not enhance the accuracy on its own
- Combining it with an argumentative score approach improves the accuracy score extensively
- Evaluation of all approaches of argumentativeness Computation:
- Claim probability score approach: Not enhances the accuracy on its own
- Combining it with an argumentative score approach improves the accuracy score extensively

![image](https://user-images.githubusercontent.com/38283252/146688695-b19674d6-70d8-494e-913d-d20924595153.png)
 



-Hybrid Score Approach: Increasedin accuracy by 11% then baseline

### 3. Topic-wise Snippet Generation Evaluation (0 < d < 1)

- Integration of both tasks for snippet generation
- Argument Context Matrix: [1,0,1] 
- M: 200
- Argumentativeness Computation method: Hybrid Score Approach
- Optimal Value of damping d : 0.2

![image](https://user-images.githubusercontent.com/38283252/146688356-91dcb072-8d59-4158-a848-48fbe89d31df.png)

- Evaluation of Snippet Generation for each query topic in the test set
- Snippet Generation: Evaluation against previous approach   (**Gain 9% Overall**)

![image](https://user-images.githubusercontent.com/38283252/146688368-5dbe8cde-dec4-4884-8992-79483a68d0e7.png)

## References

1. Milad Alshomary, Nick Düsterhus, and Henning Wachsmuth. 2020. Extractive snippet generation for arguments. In Proceedings of the 43rd International ACM SIGIR Conference on Research and Development in Information Retrieval. ACM,

2. Yamen Ajjour, Henning Wachsmuth, Johannes Kiesel, Martin Potthast, Matthias Hagen, and Benno
Stein. 2019b. Data Acquisition for Argument Search: The args.me corpus. In 42nd German Conference on Artificial Intelligence (KI 2019), pages 48–59, Berlin Heidelberg New York. Springer.

3. Lawrence Page, Sergey Brin, Rajeev Motwani, and Terry Winograd. 1999. The PageRank citation ranking: Bringing order to the web. Technical report, Stanford InfoLab.

4. Yamen Ajjour, Henning Wachsmuth, Dora Kiesel, Patrick Riehmann, Fan Fan, Giuliano Castiglia, Rosemary Adejoh, Bernd Fröhlich, and Benno Stein. 2018. Visualization of the topic space of argument search results in args. me. In Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing: System Demonstrations, pages 60–65.

5. Tuhin Chakrabarty, Christopher Hidey, and Kathleen McKeown. 2019. Imho fine-tuning improves claim detection. arXiv preprint arXiv:1905.07000. 

6. https://huggingface.co/chkla/roberta-argument

7. Stab, Christian, Tristan Miller, and Iryna Gurevych. "Cross-topic argument mining from heterogeneous sources using attention-based neural networks." arXiv preprint arXiv:1802.05758  (2018).

