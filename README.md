# Hacklytics 2024 Assurant Challenge 1

The idea is to create multi-modal (image and text) summaries from the multi-model data customers submit in house damage claims. We developed a multi-modal Gen AI model which takes the input in the format of a text and list of images and answers below questions -

1) What is the summary of the claim?
2) What are the immediate issues in the house that need attention?
3) What are the long term issues in the house?
4) What are the next steps to be taken to fix these issues?

By answering above questions this multi-modal AI assistant will help the insurance agents guiding the customers about their house repair.

## Idea and approach

As the input is both image data and text data and output is summarizing these two types of data, we decided to built a multi-modal Gen AI model. We will train the model with image, text pairs and aim to make the model learn similar vector representation for image, text pairs. During the inference stage, we will encode both the images and text into vectors, aggregate them and finally decode the aggregated vector into a summarized text. 

For making the summarized text to answer above specific questions about potential issues, we decided to use few-shot prompting and making api call to GPT-4 to get the answers to the questions. Few-shot prompting makes the answers tailored to image and text provided. 

## Dataset

We created a small dataset from webscraping from new articles about natural calamities to create text and image pairs. From the image dataset provided of damaged exterior and interior photos, we used GPT-4 to get text descriptions of the images and used these text and image pairs also for training our model.

## More on how the model is built

The model is built on  intel dev cloud enviroment. The final model is open-sourced  on hugginggface for public usage. We used the Blip-Image-Captioning-Large as the pre-trained model and fine-tuned on a custom dataset created from the images provided by Assurant. The model was fine-tuned for 10 epochs using AdamW optimizer and
has been pushed to Huggingface. We then use the Huggingface serverless inference endpoint to use our model.
The jupyter-notebook that we used for fine-tuning is provided in this repository.

## Website

We created a python web-server based on flask and deployed it in AWS. The website contains a sign-up/login page for users. A claim form in which the users can submit their claims - in which they submit the text claim and upload images showing their house. A webpage showing the summary and the answers to the questions based on the claim form submitted. 



