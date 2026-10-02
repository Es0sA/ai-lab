import os

BASE = '/home/ubuntu/ai-lab/weeks'

def week_page(filename, weekid, badge, title, dates, desc, total, objectives, sections, prev_link, prev_label, next_link, next_label):
    obj_items = '\n'.join(f'      <li>{o}</li>' for o in objectives)
    sections_html = ''
    for sec in sections:
        sec_title = sec['title']
        items_html = ''
        for item in sec['items']:
            note_html = f'<div class="resource-note">{item["note"]}</div>' if item.get('note') else ''
            items_html += f'''
    <div class="resource-item">
      <input type="checkbox" class="resource-checkbox" data-id="{item['id']}">
      <div class="resource-body">
        <div class="resource-title-row">
          <span class="resource-title">{item['title']}</span>
          <span class="tag tag-{item['tag']}">{item['tag'].title()}</span>
        </div>
        <div class="resource-meta">{item['meta']}</div>
        {note_html}
      </div>
    </div>'''
        sections_html += f'''
  <div class="section-title">{sec_title}</div>
  <div class="resource-list">{items_html}
  </div>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{badge}: {title} | AI Lab</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/styles.css">
</head>
<body>
<nav class="navbar">
  <a class="navbar-brand" href="../index.html"><div class="logo-icon">AI</div>AI Lab</a>
  <div class="navbar-links">
    <a href="../index.html">Dashboard</a>
    <a href="../resources.html">All Resources</a>
  </div>
</nav>
<div class="container">
  <div class="week-detail-header">
    <div class="week-detail-meta">
      <span class="week-badge">{badge}</span>
      <span style="color:var(--text-muted);font-size:13px;">{dates}</span>
    </div>
    <div class="week-detail-title">{title}</div>
    <div class="week-detail-desc">{desc}</div>
    <div class="week-detail-progress" style="margin-top:16px;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
        <span style="font-size:13px;color:var(--text-muted);">Progress: <span id="week-checked">0</span> / <span id="week-total">{total}</span></span>
        <span style="font-weight:700;color:var(--accent);font-family:var(--font-mono);" id="week-pct">0%</span>
      </div>
      <div class="progress-bar-bg"><div class="progress-bar-fill" id="week-bar" style="width:0%"></div></div>
    </div>
  </div>
  <div class="objectives-card">
    <h3>Learning Objectives</h3>
    <ul>
{obj_items}
    </ul>
  </div>
{sections_html}
  <div class="page-nav">
    <a class="btn btn-ghost" href="{prev_link}">&larr; {prev_label}</a>
    <a class="btn btn-primary" href="{next_link}">{next_label} &rarr;</a>
  </div>
</div>
<script src="../js/progress.js"></script>
<script>document.addEventListener('DOMContentLoaded', () => initCheckboxes('{weekid}'));</script>
</body>
</html>'''
    path = os.path.join(BASE, filename)
    with open(path, 'w') as f:
        f.write(html)
    print(f'Written: {path}')

# ---- WEEK 3 ----
week_page('w3.html','w3','Week 3','Data Exploration: Clustering, PCA &amp; Time Series','Oct 17 &mdash; Oct 23, 2026',
'Apply clustering and dimensionality reduction techniques to segment data and extract meaningful patterns. Also covers Time Series fundamentals: trend, seasonality, and forecasting.',
8,
['Perform K-Means and K-Medoids clustering on a real dataset in KNIME','Explain PCA and t-SNE in plain language','Interpret a dendrogram and choose the right number of clusters','Identify trend and seasonality in time series data','Build your first KNIME workflow from scratch'],
[
  {'title':'Videos','items':[
    {'id':'w3-v1','title':'K-Means Clustering Clearly Explained','tag':'video','meta':'YouTube &mdash; StatQuest (Josh Starmer) &mdash; <a href="https://www.youtube.com/watch?v=4b5d3muPQmA" target="_blank">Watch</a> &mdash; 9 min','note':'The clearest explanation of K-Means anywhere. StatQuest is your best friend for all classical ML topics this course.'},
    {'id':'w3-v2','title':'PCA Main Ideas in 5 Minutes','tag':'video','meta':'YouTube &mdash; StatQuest &mdash; <a href="https://www.youtube.com/watch?v=HMOI_lkzW08" target="_blank">Watch</a> &mdash; 5 min','note':'Intuitive visual explanation. Watch this before the longer PCA video.'},
    {'id':'w3-v3','title':'PCA Step-by-Step','tag':'video','meta':'YouTube &mdash; StatQuest &mdash; <a href="https://www.youtube.com/watch?v=FgakZw6K1QQ" target="_blank">Watch</a> &mdash; 21 min','note':'Deeper dive into how PCA is computed. Builds on the 5-minute intro.'},
    {'id':'w3-v4','title':'t-SNE Clearly Explained','tag':'video','meta':'YouTube &mdash; StatQuest &mdash; <a href="https://www.youtube.com/watch?v=NEaUSP4YerM" target="_blank">Watch</a> &mdash; 12 min','note':'t-SNE is used for visualizing high-dimensional data. Essential for understanding how AI models see data internally.'},
    {'id':'w3-v5','title':'Time Series Analysis &mdash; Decomposition','tag':'video','meta':'YouTube &mdash; ritvikmath &mdash; <a href="https://www.youtube.com/watch?v=oY-j2Wof51c" target="_blank">Watch</a> &mdash; 15 min','note':'Best explanation of trend, seasonality, and noise decomposition. Very practical, no heavy math.'},
  ]},
  {'title':'Hands-On Tool (KNIME)','items':[
    {'id':'w3-k1','title':'KNIME Clustering Tutorial (Official)','tag':'tool','meta':'KNIME Learning Hub &mdash; <a href="https://www.knime.com/learning" target="_blank">Start Free Course</a>','note':'Work through the official KNIME clustering course. You will cluster a real dataset and visualize results. This is your first hands-on KNIME session.'},
    {'id':'w3-k2','title':'Case Study Dataset: Country Socio-Economic Clustering','tag':'dataset','meta':'Kaggle (Free, no login needed) &mdash; <a href="https://www.kaggle.com/datasets/rohan0301/unsupervised-learning-on-country-data" target="_blank">Download Dataset</a>','note':'This is the exact type of dataset used in the brochure\'s Public Policy case study. Load it into KNIME and apply K-Means clustering.'},
  ]},
  {'title':'Reading','items':[
    {'id':'w3-r1','title':'An Introduction to t-SNE with Python (Visual Article)','tag':'reading','meta':'Free Article &mdash; Distill.pub &mdash; <a href="https://distill.pub/2016/misread-tsne/" target="_blank">Read Free</a>','note':'Distill.pub produces the highest quality visual ML explanations online. This article shows how to correctly interpret (and misinterpret) t-SNE plots.'},
  ]},
],'w2.html','Week 2','w4.html','Week 4: Regression')

# ---- WEEK 4 ----
week_page('w4.html','w4','Week 4','Prediction Methods: Regression','Oct 24 &mdash; Oct 30, 2026',
'Build and evaluate regression models to predict numerical outcomes and identify key drivers of a target variable. Learn how to validate assumptions, interpret outputs, and run full regression workflows in KNIME.',
7,
['Explain the difference between simple and multiple linear regression','Interpret regression coefficients as business insights','Identify and handle violations of linear regression assumptions','Build a complete regression workflow in KNIME including evaluation','Apply performance metrics: R-squared, MAE, RMSE'],
[
  {'title':'Videos','items':[
    {'id':'w4-v1','title':'Linear Regression Clearly Explained','tag':'video','meta':'YouTube &mdash; StatQuest &mdash; <a href="https://www.youtube.com/watch?v=nk2CQITm_eo" target="_blank">Watch</a> &mdash; 27 min','note':'The definitive StatQuest video on linear regression. Covers the math intuitively with no heavy algebra required.'},
    {'id':'w4-v2','title':'Multiple Regression Clearly Explained','tag':'video','meta':'YouTube &mdash; StatQuest &mdash; <a href="https://www.youtube.com/watch?v=EkAQAi3a4js" target="_blank">Watch</a> &mdash; 9 min','note':'Extends the single variable regression to multiple predictors. Directly relevant to the streaming viewership and booking cancellation projects.'},
    {'id':'w4-v3','title':'R-Squared and Adjusted R-Squared Explained','tag':'video','meta':'YouTube &mdash; StatQuest &mdash; <a href="https://www.youtube.com/watch?v=2AQKmw14mHM" target="_blank">Watch</a> &mdash; 11 min','note':'Critical for evaluating how good your regression model actually is.'},
    {'id':'w4-v4','title':'Gradient Descent, Step by Step','tag':'video','meta':'YouTube &mdash; StatQuest &mdash; <a href="https://www.youtube.com/watch?v=sDv4f4s2SB8" target="_blank">Watch</a> &mdash; 24 min','note':'Gradient descent is the optimization algorithm behind most ML training. Understanding it conceptually is essential before Phase 2 (LLMs).'},
  ]},
  {'title':'Hands-On Tool (KNIME)','items':[
    {'id':'w4-k1','title':'KNIME Regression Workflow Tutorial','tag':'tool','meta':'KNIME Hub &mdash; <a href="https://www.knime.com/community" target="_blank">Browse Workflows</a>','note':'Search "regression" on KNIME Hub and download the Linear Regression Example workflow. Open it in KNIME, run it, modify the target variable, and observe how the metrics change.'},
    {'id':'w4-k2','title':'Case Study Dataset: Streaming Viewership Analysis','tag':'dataset','meta':'Use the Media & Entertainment dataset from the brochure. Proxy: <a href="https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.csv" target="_blank">Netflix Dataset on Kaggle</a>','note':'Apply linear regression to predict viewership or engagement. Match the Media & Entertainment case study from the brochure.'},
  ]},
  {'title':'Reading','items':[
    {'id':'w4-r1','title':'Interpreting Linear Regression Coefficients (Plain English)','tag':'reading','meta':'Free Article &mdash; Towards Data Science &mdash; <a href="https://towardsdatascience.com/interpreting-coefficients-in-linear-regression-models-part-1-9f7ffe34ee66" target="_blank">Read Free</a>','note':'Bridges theory and business communication. After reading, you should be able to explain regression results to a non-technical stakeholder.'},
  ]},
],'w3.html','Week 3','w5.html','Week 5: Classification')

# ---- WEEK 5 ----
week_page('w5.html','w5','Week 5','Classification, Explainability &amp; Deep Learning Bridge','Oct 31 &mdash; Nov 6, 2026',
'Build and evaluate classification models using Decision Trees, Random Forests, and Gradient Boosting in KNIME. Learn to explain model decisions to non-technical stakeholders. Bridge into Deep Learning by understanding neural network structure conceptually.',
8,
['Build a decision tree and read its rules as business logic','Explain why Random Forests outperform single trees','Interpret a confusion matrix, precision, recall, and F1-score','Use SHAP values to explain individual AI predictions','Understand neural network layers and activation functions at a conceptual level'],
[
  {'title':'Videos','items':[
    {'id':'w5-v1','title':'Decision Trees Clearly Explained','tag':'video','meta':'YouTube &mdash; StatQuest &mdash; <a href="https://www.youtube.com/watch?v=7VeUPuFGJHk" target="_blank">Watch</a> &mdash; 18 min','note':'Decision trees are the most interpretable ML model. Master this before random forests.'},
    {'id':'w5-v2','title':'Random Forests: Part 1 &mdash; Building and Using','tag':'video','meta':'YouTube &mdash; StatQuest &mdash; <a href="https://www.youtube.com/watch?v=J4Wdy0Wc_xQ" target="_blank">Watch</a> &mdash; 10 min','note':'Explains how bagging multiple trees reduces overfitting. Directly used in the Hospitality booking cancellation project.'},
    {'id':'w5-v3','title':'Gradient Boost (XGBoost) Part 1: Regression','tag':'video','meta':'YouTube &mdash; StatQuest &mdash; <a href="https://www.youtube.com/watch?v=3CC4N4z3GJc" target="_blank">Watch</a> &mdash; 22 min','note':'XGBoost consistently wins Kaggle competitions on tabular data. Understanding it conceptually is important even in a no-code context.'},
    {'id':'w5-v4','title':'Confusion Matrix Clearly Explained','tag':'video','meta':'YouTube &mdash; StatQuest &mdash; <a href="https://www.youtube.com/watch?v=Kdsp6soqA7o" target="_blank">Watch</a> &mdash; 7 min','note':'Essential for understanding whether your classifier is actually doing what you think.'},
    {'id':'w5-v5','title':'Neural Networks Part 1: Inside the Black Box','tag':'video','meta':'YouTube &mdash; StatQuest &mdash; <a href="https://www.youtube.com/watch?v=CqOfi41LfDw" target="_blank">Watch</a> &mdash; 20 min','note':'This is your Deep Learning bridge. Conceptual intro to layers, weights, and activation functions. Sets you up perfectly for Week 6.'},
  ]},
  {'title':'Hands-On Tool (KNIME)','items':[
    {'id':'w5-k1','title':'KNIME Classification Workflow (Random Forest)','tag':'tool','meta':'KNIME Hub &mdash; <a href="https://www.knime.com/community" target="_blank">Browse Workflows</a>','note':'Download and run the Random Forest classification workflow on KNIME Hub. Switch the dataset to the hotel booking dataset.'},
    {'id':'w5-k2','title':'Case Study Dataset: Hotel Booking Cancellation','tag':'dataset','meta':'Kaggle Free &mdash; <a href="https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand" target="_blank">Download Dataset</a>','note':'This is the exact Hospitality project from the brochure. Predict which bookings will be cancelled using Random Forest in KNIME.'},
  ]},
  {'title':'Reading','items':[
    {'id':'w5-r1','title':'SHAP Values Explained (Explainable AI)','tag':'reading','meta':'Free Article &mdash; Towards Data Science &mdash; <a href="https://towardsdatascience.com/shap-explained-the-way-i-wish-someone-explained-it-to-me-ab81cc69ef30" target="_blank">Read Free</a>','note':'SHAP (SHapley Additive exPlanations) is the standard way to explain any ML model\'s predictions. This is what regulators and managers ask for.'},
  ]},
],'w4.html','Week 4','w6.html','Week 6: GenAI Mechanics')

# ---- WEEK 6 ----
week_page('w6.html','w6','Week 6','AI Design Thinking + GenAI Mechanics + Ethical AI','Nov 7 &mdash; Nov 13, 2026',
'Learn to frame business problems correctly before reaching for an AI solution. Understand how Transformer architecture enables generative AI. Revisit ethical AI with real bias case studies and practical audit techniques.',
8,
['Frame any business problem into the correct AI architecture before building','Understand the Transformer architecture at a conceptual level','Explain what training data, fine-tuning, and RLHF mean','Identify where bias can enter an AI system and how to audit for it','Apply a simple hallucination detection checklist'],
[
  {'title':'Videos','items':[
    {'id':'w6-v1','title':'Transformers: The Architecture That Changed Everything','tag':'video','meta':'YouTube &mdash; Andrej Karpathy &mdash; <a href="https://www.youtube.com/watch?v=kCc8FmEb1nY" target="_blank">Watch</a> &mdash; First 60 min only','note':'Karpathy builds a small GPT from scratch. Watch the first hour for the conceptual arc. You do not need to understand every line of code.'},
    {'id':'w6-v2','title':'AI Alignment &mdash; Why It Is Hard','tag':'video','meta':'YouTube &mdash; Robert Miles &mdash; <a href="https://www.youtube.com/watch?v=pYXy-A4siMw" target="_blank">Watch</a> &mdash; 20 min','note':'Explains hallucination, alignment, and why LLMs sometimes behave unexpectedly. Essential context before building GenAI workflows.'},
    {'id':'w6-v3','title':'Responsible AI Practices (Google)','tag':'video','meta':'YouTube &mdash; Google Cloud Tech &mdash; <a href="https://www.youtube.com/watch?v=aGwYtUzMQUk" target="_blank">Watch</a> &mdash; 15 min','note':'Practical overview of fairness, accountability, and transparency in AI systems.'},
  ]},
  {'title':'Courses (Free)','items':[
    {'id':'w6-c1','title':'Evaluating and Debugging Generative AI (Full)','tag':'course','meta':'Free &mdash; DeepLearning.AI &mdash; <a href="https://www.deeplearning.ai/short-courses/evaluating-debugging-generative-ai/" target="_blank">Enroll Free</a> &mdash; ~1 hr','note':'Start this course this week. It covers how to detect hallucinations and evaluate GenAI output quality systematically.'},
  ]},
  {'title':'Reading','items':[
    {'id':'w6-r1','title':'The Illustrated GPT-2','tag':'reading','meta':'Free Blog &mdash; Jay Alammar &mdash; <a href="https://jalammar.github.io/illustrated-gpt2/" target="_blank">Read Free</a>','note':'Companion to the Illustrated Transformer. Shows how GPT generates text token by token. Read the "Language Modeling" and "The GPT-2 Model" sections.'},
    {'id':'w6-r2','title':'AI Fairness 101 &mdash; Google PAIR','tag':'reading','meta':'Free Resource &mdash; Google &mdash; <a href="https://pair.withgoogle.com/explorables/measuring-fairness/" target="_blank">Explore Free</a>','note':'Interactive explainable that lets you explore fairness metrics hands-on. Spend 20 minutes playing with the tool.'},
    {'id':'w6-r3','title':'Attention Is All You Need (Original Paper &mdash; Abstract + Section 3 only)','tag':'paper','meta':'Free &mdash; arXiv &mdash; <a href="https://arxiv.org/abs/1706.03762" target="_blank">Read Free</a>','note':'You do not need to understand every equation. Read the Abstract, Introduction, and Section 3 (Model Architecture). Understand the high-level diagram.'},
  ]},
],'w5.html','Week 5','w7.html','Week 7: Advanced Prompting')

# ---- WEEK 7 ----
week_page('w7.html','w7','Week 7','Advanced Prompt Engineering &amp; Structured Outputs','Nov 14 &mdash; Nov 20, 2026',
'Master advanced prompt patterns that produce reliable, production-grade outputs from any LLM. Learn to force structured JSON outputs, compare model capabilities, and build your reusable prompt template library.',
7,
['Apply ReAct, Tree-of-Thought, and Self-Consistency prompt patterns','Force any LLM to return clean JSON output reliably, every time','Compare Llama, Mistral, Gemini, and Claude for different task types','Build a personal 10-template prompt library for your specific work domain','Identify when a prompt is likely to fail and why'],
[
  {'title':'Courses (Free)','items':[
    {'id':'w7-c1','title':'Building Systems with the ChatGPT API','tag':'course','meta':'Free &mdash; DeepLearning.AI &mdash; <a href="https://www.deeplearning.ai/short-courses/building-systems-with-chatgpt/" target="_blank">Enroll Free</a> &mdash; ~1.5 hrs','note':'Covers chaining prompts, building multi-step LLM pipelines, and classifying inputs before sending to an LLM. Complete all lessons.'},
    {'id':'w7-c2','title':'Prompt Engineering with Llama 2 &amp; 3','tag':'course','meta':'Free &mdash; DeepLearning.AI &mdash; <a href="https://www.deeplearning.ai/short-courses/prompt-engineering-with-llama-2/" target="_blank">Enroll Free</a> &mdash; ~1 hr','note':'Learn prompt engineering with an open-source LLM. Important because Llama models are what Groq (your free LLM provider) runs.'},
  ]},
  {'title':'Reading &amp; Reference','items':[
    {'id':'w7-r1','title':'Chain-of-Thought Prompting Elicits Reasoning in LLMs (Original Paper)','tag':'paper','meta':'Free &mdash; arXiv &mdash; <a href="https://arxiv.org/abs/2201.11903" target="_blank">Read Abstract + Examples</a>','note':'Read the Abstract and look at the examples in Figure 1. You will instantly understand why CoT prompting makes LLMs dramatically more reliable on reasoning tasks.'},
    {'id':'w7-r2','title':'OpenAI Prompt Engineering Best Practices','tag':'reading','meta':'Free Guide &mdash; OpenAI &mdash; <a href="https://platform.openai.com/docs/guides/prompt-engineering" target="_blank">Read Free</a>','note':'Official, concise, and practical. Read all 6 strategies. These are tool-agnostic and apply to any LLM you use.'},
    {'id':'w7-r3','title':'Model Comparison Reference (Free LLMs)','tag':'reading','meta':'Free Tool &mdash; LMSys Chatbot Arena &mdash; <a href="https://arena.ai" target="_blank">Explore</a>','note':'An open benchmark where community members blind-test LLMs. Look at the leaderboard to understand which free models perform best on different task types.'},
  ]},
  {'title':'Hands-On Exercise','items':[
    {'id':'w7-e1','title':'Build Your Personal Prompt Library (10 Templates)','tag':'tool','meta':'Use Groq Playground (free) &mdash; <a href="https://console.groq.com/playground" target="_blank">Open Playground</a>','note':'Using Groq\'s free playground, write and test 10 prompt templates for your own work context. Save them in a local text file or Notion doc. This is your most reusable deliverable from the entire course.'},
  ]},
],'w6.html','Week 6','w8.html','Week 8: Computer Vision & n8n')

# ---- WEEK 8 ----
week_page('w8.html','w8','Week 8','Computer Vision, Model Comparison &amp; n8n Automation','Nov 21 &mdash; Nov 27, 2026',
'Explore how AI interprets visual data using convolutional neural networks. Train a no-code image classifier with Google Teachable Machine. Introduction to n8n for automating AI workflow outputs.',
7,
['Train a working image classifier with zero code using Teachable Machine','Explain what a CNN does differently from a regular neural network','Trigger an automated workflow in n8n based on AI output','Connect n8n to a free LLM API and log outputs to a Google Sheet','Understand when to use vision AI vs text AI for a given problem'],
[
  {'title':'Videos','items':[
    {'id':'w8-v1','title':'Convolutional Neural Networks (CNNs) Visually Explained','tag':'video','meta':'YouTube &mdash; 3Blue1Brown &mdash; <a href="https://www.youtube.com/watch?v=KuXjwB4LzSA" target="_blank">Watch</a> &mdash; 24 min','note':'The clearest explanation of how CNNs detect patterns in images. Understand this before trying Teachable Machine.'},
    {'id':'w8-v2','title':'n8n Crash Course for Beginners','tag':'video','meta':'YouTube &mdash; n8n &mdash; <a href="https://www.youtube.com/watch?v=1MwSoB0gnM4" target="_blank">Watch</a> &mdash; 30 min','note':'Official n8n walkthrough. By end of this video you will have built your first automated workflow. Use n8n Desktop App on Windows.'},
  ]},
  {'title':'Hands-On Tools','items':[
    {'id':'w8-t1','title':'Google Teachable Machine (No-Code Image Classifier)','tag':'tool','meta':'Free Browser Tool &mdash; <a href="https://teachablemachine.withgoogle.com/" target="_blank">Open Teachable Machine</a>','note':'Train a working image classifier directly in your browser with no code. Upload sample photos from your phone, train it, and test it. Takes about 20 minutes to get a working model.'},
    {'id':'w8-t2','title':'n8n: Build Your First LLM Automation Workflow','tag':'tool','meta':'n8n Desktop App &mdash; Tutorial: <a href="https://docs.n8n.io/try-it-out/quickstart/" target="_blank">Quickstart Guide</a>','note':'Build a workflow that: (1) accepts a text input, (2) sends it to Groq (free LLM), and (3) saves the output to a Google Sheet. This is your first real AI automation.'},
  ]},
  {'title':'Reading','items':[
    {'id':'w8-r1','title':'How Google Lens Works (Practical Computer Vision Overview)','tag':'reading','meta':'Free Article &mdash; Google AI Blog &mdash; <a href="https://ai.googleblog.com/2017/02/on-device-machine-intelligence.html" target="_blank">Read Free</a>','note':'Practical context for where computer vision is deployed today. Connects the CNN theory to real applications.'},
    {'id':'w8-r2','title':'The Roboflow Computer Vision Tutorial','tag':'reading','meta':'Free Guide &mdash; Roboflow &mdash; <a href="https://roboflow.com/learn" target="_blank">Browse Tutorials</a>','note':'Roboflow is a free no-code computer vision platform. Browse the tutorials to understand object detection use cases beyond image classification.'},
  ]},
],'w7.html','Week 7','w9.html','Week 9: RAG Foundations')

# ---- WEEK 9 ----
week_page('w9.html','w9','Week 9','RAG Foundations: Embeddings, Chunking &amp; Vector Stores','Nov 28 &mdash; Dec 4, 2026',
'Build Retrieval-Augmented Generation (RAG) pipelines that connect LLMs to external knowledge sources for grounded, reliable outputs. Understand embeddings, chunking strategies, and vector databases. Automate outputs with n8n.',
8,
['Explain what an embedding is and why it enables semantic search','Choose the right chunking strategy for different document types','Set up a working RAG pipeline in Dify with a free vector database','Connect the RAG output to n8n to trigger automated actions','Understand the difference between keyword search and semantic search'],
[
  {'title':'Courses (Free)','items':[
    {'id':'w9-c1','title':'Building and Evaluating Advanced RAG','tag':'course','meta':'Free &mdash; DeepLearning.AI &mdash; <a href="https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/" target="_blank">Enroll Free</a> &mdash; ~1.5 hrs','note':'The best structured introduction to RAG available for free. Covers sentence window retrieval, auto-merging retrieval, and RAG triad evaluation. Complete all lessons this week.'},
    {'id':'w9-c2','title':'Vector Databases: From Embeddings to Applications','tag':'course','meta':'Free &mdash; DeepLearning.AI &mdash; <a href="https://www.deeplearning.ai/short-courses/vector-databases-embeddings-applications/" target="_blank">Enroll Free</a> &mdash; ~1 hr','note':'Covers how vector databases store and retrieve embeddings. Directly needed to understand the storage layer of your RAG pipeline.'},
  ]},
  {'title':'Hands-On Tools','items':[
    {'id':'w9-t1','title':'Dify: Build Your First RAG Pipeline','tag':'tool','meta':'Free &mdash; <a href="https://dify.ai" target="_blank">dify.ai</a> &mdash; Tutorial: <a href="https://docs.dify.ai/getting-started" target="_blank">Getting Started Guide</a>','note':'Build a document Q&A chatbot in Dify: upload a PDF, embed it with a free embedding model, store in a local vector store, and query it with a Groq LLM. No code needed.'},
    {'id':'w9-t2','title':'Case Study Dataset: Public Company Annual Report (PDF)','tag':'dataset','meta':'Free &mdash; SEC EDGAR &mdash; <a href="https://www.annualreports.com" target="_blank">Download Any 10-K Report</a>','note':'This is your Financial Report Analyzer project data source. Download any company\'s annual 10-K report as a PDF. The RAG pipeline you build here will be the Week 11 project.'},
  ]},
  {'title':'Reading &amp; Papers','items':[
    {'id':'w9-r1','title':'RAG: Retrieval-Augmented Generation (Original Paper)','tag':'paper','meta':'Free &mdash; arXiv (Facebook AI) &mdash; <a href="https://arxiv.org/abs/2005.11401" target="_blank">Read Abstract &amp; Introduction</a>','note':'The original 2020 Facebook AI paper that introduced RAG. Read the Abstract, Introduction, and Section 2. Understanding the core idea from the source is valuable context.'},
    {'id':'w9-r2','title':'Chunking Strategies for LLM Applications','tag':'reading','meta':'Free Article &mdash; Pinecone &mdash; <a href="https://www.pinecone.io/learn/chunking-strategies/" target="_blank">Read Free</a>','note':'The definitive practical guide to choosing chunk sizes and overlap strategies. This single decision affects your RAG accuracy more than any other parameter.'},
    {'id':'w9-r3','title':'What Are Embeddings?','tag':'reading','meta':'Free Article &mdash; Vicki Boykis &mdash; <a href="https://vickiboykis.com/what_are_embeddings/" target="_blank">Read Free</a>','note':'The clearest long-form explanation of embeddings written for a technical but non-specialist audience. Read Chapters 1 to 3.'},
  ]},
],'w8.html','Week 8','w10.html','Week 10: RAG Evaluation')

# ---- WEEK 10 ----
week_page('w10.html','w10','Week 10','RAG Evaluation, Citation Tracing &amp; Security','Dec 5 &mdash; Dec 11, 2026',
'Evaluate RAG pipeline quality systematically using LLM-as-a-judge, hallucination detection, and consistency checks. Implement source citation so the system shows users exactly which document it pulled from. Understand RAG security risks.',
7,
['Evaluate a RAG pipeline using the RAG Triad: Context Relevance, Groundedness, Answer Relevance','Implement citation and source-page tracing in Dify','Detect hallucinations using consistency checking techniques','Understand prompt injection risks in RAG systems','Optimize prompts for better retrieval accuracy'],
[
  {'title':'Courses (Free)','items':[
    {'id':'w10-c1','title':'Evaluating and Debugging Generative AI (Complete)','tag':'course','meta':'Free &mdash; DeepLearning.AI &mdash; <a href="https://www.deeplearning.ai/short-courses/evaluating-debugging-generative-ai/" target="_blank">Enroll Free</a> &mdash; ~1 hr','note':'Complete any remaining lessons from Week 6. Focus on the evaluation sections: tracing, evaluation metrics, and debugging.'},
  ]},
  {'title':'Reading &amp; Papers','items':[
    {'id':'w10-r1','title':'RAGAS: Automated Evaluation of RAG Pipelines','tag':'paper','meta':'Free &mdash; arXiv &mdash; <a href="https://arxiv.org/abs/2309.15217" target="_blank">Read Abstract &amp; Section 3</a>','note':'RAGAS is the standard open-source framework for evaluating RAG systems. Read the Abstract and Section 3 to understand the three evaluation metrics: faithfulness, answer relevance, context precision.'},
    {'id':'w10-r2','title':'Prompt Injection Attacks in LLM Applications','tag':'reading','meta':'Free Article &mdash; Simon Willison &mdash; <a href="https://simonwillison.net/2022/Sep/12/prompt-injection/" target="_blank">Read Free</a>','note':'Prompt injection is the most important RAG security risk. This is the original article that named and defined the problem. Essential reading before deploying any RAG system.'},
    {'id':'w10-r3','title':'Building Trustworthy AI: Source Attribution in RAG','tag':'reading','meta':'Free Article &mdash; LangChain Blog &mdash; <a href="https://blog.langchain.dev/semi-structured-multi-modal-rag/" target="_blank">Read Free</a>','note':'Practical techniques for making your RAG system show users which specific chunk and page it retrieved from. This is what transforms a demo into a trustworthy business tool.'},
  ]},
  {'title':'Hands-On Exercise','items':[
    {'id':'w10-e1','title':'Evaluate Your Week 9 RAG Pipeline with RAGAS Metrics','tag':'tool','meta':'Use Dify evaluation + RAGAS &mdash; <a href="https://docs.dify.ai/guides/monitoring" target="_blank">Dify Evaluation Docs</a>','note':'Run your Week 9 Financial Report RAG pipeline through a set of 10 test questions. Score it on faithfulness and relevance. Document what breaks and why. This feeds directly into the Week 11 project.'},
    {'id':'w10-e2','title':'Add Citation Tracing to Your Dify RAG Pipeline','tag':'tool','meta':'Dify Docs &mdash; <a href="https://docs.dify.ai" target="_blank">docs.dify.ai</a>','note':'Configure Dify to return the source document name and page number alongside every answer. Test that citations are accurate.'},
  ]},
],'w9.html','Week 9','w11.html','Week 11: Project')

# ---- WEEK 11 ----
week_page('w11.html','w11','Week 11','Project: Financial Report Analyzer','Dec 12 &mdash; Dec 18, 2026',
'Build the Financial Report Analyzer capstone project. A complete RAG pipeline that extracts key information from lengthy annual reports to improve decision-making efficiency. This project combines Weeks 9 and 10 into a single deployable system.',
5,
['Load and chunk a real company annual report PDF into a vector store','Query the document with natural language business questions','Validate answers with citation tracing back to source pages','Detect and handle hallucinated answers using consistency checks','Document the project: problem, approach, results, and limitations'],
[
  {'title':'Project Resources','items':[
    {'id':'w11-p1','title':'SEC EDGAR: Download Annual Report (10-K)','tag':'dataset','meta':'Free &mdash; <a href="https://www.annualreports.com" target="_blank">Browse Reports</a>','note':'Choose any well-known company (Apple, Tesla, Microsoft). Download their most recent 10-K annual report as a PDF. This is your RAG document.'},
    {'id':'w11-p2','title':'Dify: Complete RAG Pipeline Setup','tag':'tool','meta':'<a href="https://dify.ai" target="_blank">dify.ai</a> &mdash; <a href="https://docs.dify.ai" target="_blank">Documentation</a>','note':'Build the full pipeline: PDF loader → text splitter → embedding model (free) → vector store → LLM (Groq free) → chat interface with citations.'},
    {'id':'w11-p3','title':'Project Test Questions (Business Analyst Perspective)','tag':'reading','meta':'Create your own 15 test questions','note':'Write 15 questions a financial analyst would ask: revenue growth, key risks, segment performance, management outlook, capital allocation. Test every one and document accuracy.'},
  ]},
  {'title':'Documentation Template','items':[
    {'id':'w11-d1','title':'Project Write-Up Template','tag':'reading','meta':'Use Notion (free) or Google Docs &mdash; <a href="https://notion.so" target="_blank">notion.so</a>','note':'Document: (1) Problem Statement, (2) System Architecture diagram, (3) Tools used, (4) Evaluation results table, (5) Key findings, (6) What failed and why, (7) What you would improve. This becomes a portfolio piece.'},
    {'id':'w11-d2','title':'Draw Your System Architecture','tag':'tool','meta':'Free Diagram Tool &mdash; <a href="https://excalidraw.com" target="_blank">excalidraw.com</a>','note':'Draw a simple architecture diagram showing how the system works: PDF → Chunks → Embeddings → Vector DB → Query → LLM → Answer + Citation. This visual goes in your portfolio.'},
  ]},
],'w10.html','Week 10','w12.html','Week 12: Agentic AI')

# ---- WEEK 12 ----
week_page('w12.html','w12','Week 12','Single &amp; Multi-Agent Systems: Design, Memory &amp; Orchestration','Dec 19 &mdash; Dec 25, 2026',
'Design and deploy AI agents that can plan, remember, use tools, and complete multi-step business tasks autonomously. Extend to multi-agent systems where agents collaborate, hand off tasks, and handle real-world complexity.',
8,
['Explain the agent loop: perceive, think, act, observe','Configure memory, tools, and planning in a single Dify agent','Design a multi-agent system with a supervisor and worker agents','Implement tool accuracy evaluation for agent outputs','Apply guardrails to prevent agents from taking harmful or incorrect actions'],
[
  {'title':'Courses (Free)','items':[
    {'id':'w12-c1','title':'AI Agents in LangGraph','tag':'course','meta':'Free &mdash; DeepLearning.AI &mdash; <a href="https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/" target="_blank">Enroll Free</a> &mdash; ~2 hrs','note':'The best free course on building single and multi-agent systems. Covers state machines, memory, tool use, and human-in-the-loop. Complete all lessons.'},
    {'id':'w12-c2','title':'Building Agentic RAG with LlamaIndex','tag':'course','meta':'Free &mdash; DeepLearning.AI &mdash; <a href="https://www.deeplearning.ai/short-courses/building-agentic-rag-with-llamaindex/" target="_blank">Enroll Free</a> &mdash; ~1 hr','note':'Extends RAG into an agentic system that can decide which knowledge source to query. Directly relevant to the Week 13 Helpdesk project.'},
  ]},
  {'title':'Reading &amp; Papers','items':[
    {'id':'w12-r1','title':'ReAct: Synergizing Reasoning and Acting in LLMs','tag':'paper','meta':'Free &mdash; arXiv &mdash; <a href="https://arxiv.org/abs/2210.03629" target="_blank">Read Abstract &amp; Section 2</a>','note':'ReAct is the foundational algorithm behind most LLM agents. Read the Abstract and Section 2. The examples in the paper are the clearest illustrations of how an agent thinks step by step.'},
    {'id':'w12-r2','title':'Practices for Governing Agentic AI Systems','tag':'reading','meta':'Free &mdash; OpenAI &mdash; <a href="https://arxiv.org/abs/2402.14924" target="_blank">Read Free</a>','note':'OpenAI\'s framework for safe agentic AI deployment. Essential reading on guardrails, human-in-the-loop requirements, and when NOT to give an agent full autonomy.'},
    {'id':'w12-r3','title':'LLM Powered Autonomous Agents (Blog Post)','tag':'reading','meta':'Free &mdash; Lilian Weng / OpenAI &mdash; <a href="https://lilianweng.github.io/posts/2023-06-23-agent/" target="_blank">Read Free</a>','note':'The most comprehensive overview of LLM agent architectures. Covers planning, memory types (sensory, short-term, long-term), and tool use. Bookmark and reference throughout.'},
  ]},
  {'title':'Hands-On Tools','items':[
    {'id':'w12-t1','title':'Build a Single Agent in Dify','tag':'tool','meta':'Dify Agent Docs &mdash; <a href="https://docs.dify.ai/guides/workflow" target="_blank">Agent Flow Docs</a>','note':'Build a single agent with: (1) a tool for searching the web, (2) a tool for reading a document, and (3) memory to remember conversation context. Test it with a multi-step research task.'},
    {'id':'w12-t2','title':'Build a Multi-Agent Supervisor System in Dify','tag':'tool','meta':'Dify Multi-Agent Docs &mdash; <a href="https://docs.dify.ai" target="_blank">docs.dify.ai</a>','note':'Extend your single agent into a supervisor + 2 worker agents. The supervisor routes tasks; one worker searches knowledge, another drafts responses. This is the scaffold for the Week 13 project.'},
  ]},
],'w11.html','Week 11','w13.html','Week 13: Final Project')

# ---- WEEK 13 ----
week_page('w13.html','w13','Week 13','Project: Agentic Helpdesk + Portfolio Wrap-Up','Dec 26 &mdash; Dec 31, 2026',
'Build the Agentic Customer Support Helpdesk capstone: a multi-agent system that classifies tickets, retrieves knowledge, generates policy-compliant responses, and handles escalation. Then wrap up your portfolio with all three projects documented.',
6,
['Deploy a working multi-agent agentic helpdesk system in Dify','Implement ticket classification, RAG knowledge retrieval, and escalation routing','Evaluate agent output quality with tool accuracy metrics','Write up all three projects as business-readable case studies','Publish your portfolio to GitHub Pages or Notion'],
[
  {'title':'Project Resources','items':[
    {'id':'w13-p1','title':'Dify Multi-Agent Helpdesk Setup','tag':'tool','meta':'Dify Docs &mdash; <a href="https://docs.dify.ai/guides/workflow" target="_blank">Agent Flow Guide</a>','note':'Build the 3-agent system: (1) Classifier Agent: categorizes incoming support tickets, (2) Knowledge Agent: searches a RAG knowledge base for relevant policies, (3) Responder Agent: drafts final response or escalates.'},
    {'id':'w13-p2','title':'Sample Customer Support Dataset','tag':'dataset','meta':'Free &mdash; Kaggle &mdash; <a href="https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter" target="_blank">Download Dataset</a>','note':'Customer support conversations to test your agent system against real ticket scenarios.'},
    {'id':'w13-p3','title':'n8n: Automate Ticket Ingestion','tag':'tool','meta':'n8n Desktop App &mdash; <a href="https://docs.n8n.io" target="_blank">n8n Docs</a>','note':'Set up an n8n workflow that monitors a Gmail inbox (or webhook) for new support requests, sends them to your Dify agent, and logs the response. This makes the whole system end-to-end.'},
  ]},
  {'title':'Portfolio Wrap-Up (Bonus C)','items':[
    {'id':'w13-b1','title':'Portfolio Template: Project Case Study Format','tag':'reading','meta':'Use Notion Free or Google Docs &mdash; <a href="https://notion.so" target="_blank">notion.so</a>','note':'For each of the 3 projects write: (1) Problem Statement (1 sentence), (2) Business Impact (what decision does this enable?), (3) Architecture (your Excalidraw diagram), (4) Tools Used, (5) Results, (6) Limitations. Frame everything in business value, not technical jargon.'},
    {'id':'w13-b2','title':'Host Portfolio on GitHub Pages or Notion','tag':'tool','meta':'GitHub Pages: <a href="https://pages.github.com" target="_blank">pages.github.com</a> &mdash; or Notion Public Page: free','note':'Publish your three project write-ups publicly so you can share the URL. A public portfolio link is your proof of work for any employer, client, or collaborator.'},
    {'id':'w13-b3','title':'LinkedIn: Update Your Skills Section','tag':'reading','meta':'<a href="https://linkedin.com" target="_blank">linkedin.com</a>','note':'Add these skills: Machine Learning, Prompt Engineering, Retrieval-Augmented Generation, AI Agents, KNIME, n8n, Dify. Add a post announcing your completion of the program with your portfolio link.'},
  ]},
],'w12.html','Week 12','../index.html','Back to Dashboard')

print('All week pages written.')
