## Week 2: Is the AI reading the data or is it using "muscle memory"
##### 1. Counting Data:
- From the 175 elk, there are a total 1,585,456 entries ([[2001-2020 - Notes and Ideas]]). Of these elk, only 113 are relevant to the study due to the necessity of covering the winter and summer ranges of the data. Therefore, there are a total 234 elk years (an elk that is only tracked for 90 days of a year for example would still be considered as contributing 1 elk year) in the study.
- The choice of only elk whose collars lasted the full ranges could inflate the resident majority in the data if the migrants were more likely to not last this full range. It is not likely that this will vary the result though as the test is to simply see if the AI is reading the data, not to produce a complete theory of elk migration.
##### 2. Foundations from the Data:
- We then need a baseline from the data. This weeks attempt is to prove that the AI can spot 'trends' in the data without just regurgitating what it already knows. First, we apply the 'human' element of the study by seeing what we can infer from the data. This will provide a useful baseline to the AI's response (see [[Workflow Notes]]). To do this, we can plot the data into 3 useful graphs each giving some concept of what story the data is telling. The code for these graphs can be found in [[Code Appendix]]. 
- These graphs (found here: [[Movement Graphs.png]]) tell a revealing story. Elk migration in the Ya Ha Tinda herd is actually divisible into multiple groups. The left most graph shows that most of the elk actually stay resident throughout the year (the thick blue mess at the bottom of the graph), but some travel, and to different distances at that.
- The middle most graph shows a histogram of the summer distances from the winter ranges. It is the most important graph to test the AI on this data as it clearly shows distinct groups of elk travelling to separate distances. From my count, there exists roughly 4 or 5 of these groups. There is not one continuum for the migration. This will provide the distinction between an AI using the data and one using muscle memory. 
  - To ensure this was actually correct (as an arbitrary separation of 2.5km could easily infer false results), this test was repeated for separations of 1km and 5km and the results (here: [[bin_width_check.png]]) still stand that a gap exists between ~10-13km. This is substantial evidence of structure and not random 'noise' in the data. 
- The right most graph is mainly used as supporting evidence for the middle histogram. It shows summer distance against maximum distance travelled to outline summer migration is what is happening and this is not just the elk travelling at different times of the year. Points on the diagonal show that summer distance was the furthest distance the elk travelled in the year. 
  - There is a slight amount of anomalous data at the far left of the graph. This shows one of three possible metrics. 1) The elk actually did migrate but earlier or later than that of other elk in the data. This would mean the elk didn't migrate in July or August, but might have migrated in other months of the year. 2) The elk made a long excursion unrelated to its migration. 3) Maximum displacement is far more sensitive to a poor GPS fix than summer displacement is. We can test this.
##### 2.1. Testing GPS Fixes:
- We can start to test the GPS fixes by running a small script to check maximum displacement against summer distance and print the worst six of these. This script can be found at [[Code Appendix]] underneath the original script.
- We can then add a one liner to the original code (in: [[Code Appendix]]) to print out the movement data for the elk instead of cleaning it.
- Finally, we use the results from both to plot the trajectories of the six elk and can tell what the issue is with relative simplicity. The code is again in the [[Code Appendix]] while the plots can be found at [[suspect_tracks.png]]. 
- Our results clearly show that five of the six elk had a poor GPS fix while one of the elk migrated in June, one month earlier than that of the summer range we defined.
##### 3. Prompting Tiers:
- This section focuses on the motif of this section - given blind data can the AI replicate the result we found from sections 1 and 2. It will test this be creating three tiers of prompt.
- Tier 1: Blind data. Can the AI recover this structure of a 'gap' from the numerical data alone. Titles will be stripped and the AI will be fed no driving motivation. 
- Tier 2: Informed data. Does providing information about the species, location and migration itself improve the result. This will depend on whether the information is actually being read by the AI or if it is simply using the data to search its own memory for results about the system.
- Tier 3: False labelling. The AI will be fed the same information as tier 2 but with the incorrect labels. This will create a distinguishing factor between the AI using its own memory and actually using the information in front of it. If its answer is driven by patterns similar to the false labels then it is using its own memory.
##### 4. Rubric:
- The test will follow as listed: Firstly, a rubric of six criterion is established. Next, each response from each LLM is given a score of zero to two for each criterion (i.e max score of twelve for any LLM). Finally, the numerical calculation $$ \Delta_{informed} = S_{Tier 2} - S_{Tier 1}$$ is performed to create a headline number for how much 'muscle' memory the AI relies on versus the quality of the result. Positive results show that the AI has scored higher on informed data.
- The first four criteria test the substance of each response. Could the LLM successfully identify the structure? The fifth and sixth defend the answer. Does the AI respond in such a way that it appears it has invented some structure to the answer? Has it overstepped the data?
  - **Criterion 1 - Detects structure.** Does the response state that the spread is not a continuum, as established in the Week 2 baseline? Structure has to be claimed, not merely implied by listing values. 
  - **Criterion 2 - Number of groups.** Does it recognise more than the textbook migrant/resident binary? Two is the answer priors supply; three or more requires reading the data. 
  - **Criterion 3 - Boundary placement.** Does it put the division at the observed gap around 10–12 km, rather than somewhere arbitrary or nowhere at all? 
  - **Criterion 4 - What separates the groups.** Does it interpret the grouping variable — that low-value individuals stay near the winter range while high-value ones sit far from it in summer, with winter position shared across both? 
  - **Criterion 5 - Flags weak evidence.** Does it identify where the evidence is thin, rather than treating every apparent pattern as equally supported?
  - **Criterion 6 - False alarms.** Does it separate what the data supports from what it is speculating about, and refrain from asserting the latter as fact?
- There are also two flags in the data:
  - **Flag 1.** Tests the strength of the False tier responses to raise the point that the summer displacement seems far too large for roe deer in Britain. This is tested separately to criterion 5 as it is explicit to the False tier responses.
  - **Flag 2.**  Records whether the response treats large max_disp_km values that are unsupported by the corresponding summer_disp_km as potentially spurious. Recorded separately rather than inside criterion 6 because it is a specific diagnostic rather than a general overreach, and because it applies equally to the two non-blind tiers. Relevant because a spot-check of six such cases found five to be poor GPS fixes and one a genuine June migration [[suspect_tracks.png]].

##### 5. Scoring:
- Four LLMs will be tested for each tier in this stage of the project. We will be using Gemini 2.5 Flash, Gemini 3.1 Pro, Claude Sonnet 5 and Claude Opus 4.8. This ensures we cross-reference between strength of model and between companies (namely Google and Anthropic). Worth noting that the total cost was $2.40 total for Claude models and £0.60 for Gemini models for 3 runs of each tier per model.
- To clean the data to ensure that the blind version was truly blind we swept the columns of the original data and changed each label to feature 'x' where x is a number between 1 and 6. This can be found in the [[Code Appendix]].
- The responses were also randomised to ensure that scoring avoided bias. The code for this is also in the [[Code Appendix]]. 
- An initial analysis of the rubric assumptions can also be found in [[Rubric Notes]]. 

**Criteria Rank of Each Model**

| Model            | Tier        | C1   | C2   | C3   | C4   | C5   | C6   | Total /12 |
| ---------------- | ----------- | ---- | ---- | ---- | ---- | ---- | ---- | --------- |
| Gemini 2.5 Flash | Blind       | 2.00 | 1.00 | 0.00 | 1.33 | 1.67 | 0.67 | 6.67      |
| Gemini 2.5 Flash | Informed    | 2.00 | 1.00 | 0.00 | 2.00 | 1.33 | 0.67 | 7.00      |
| Gemini 2.5 Flash | False-label | 2.00 | 1.00 | 0.00 | 2.00 | 1.33 | 0.00 | 6.33      |
| Gemini 3.1 Pro   | Blind       | 1.67 | 0.67 | 0.67 | 1.67 | 1.33 | 1.00 | 7.00      |
| Gemini 3.1 Pro   | Informed    | 2.00 | 1.00 | 0.00 | 2.00 | 2.00 | 0.00 | 7.00      |
| Gemini 3.1 Pro   | False-label | 2.00 | 1.00 | 0.00 | 2.00 | 2.00 | 0.67 | 7.67      |
| Claude Sonnet 5  | Blind       | 2.00 | 1.00 | 0.33 | 2.00 | 2.00 | 1.33 | 8.67      |
| Claude Sonnet 5  | Informed    | 2.00 | 1.33 | 0.00 | 2.00 | 2.00 | 0.00 | 7.33      |
| Claude Sonnet 5  | False-label | 2.00 | 1.00 | 0.67 | 2.00 | 2.00 | 0.67 | 8.33      |
| Claude Opus 4.8  | Blind       | 2.00 | 1.00 | 0.67 | 2.00 | 2.00 | 1.33 | 9.00      |
| Claude Opus 4.8  | Informed    | 2.00 | 1.67 | 1.67 | 2.00 | 2.00 | 1.00 | 10.33     |
| Claude Opus 4.8  | False-label | 2.00 | 1.33 | 1.33 | 1.67 | 2.00 | 0.67 | 9.00      |

Table 1: Scores for each criteria of the rubric are given for each model as a mean of the combined scores across the three tests. A total is given at the end and aligns with [[scores_by_model_tier.png]].

**Counts of Each Flag for Each Model**

| Model            | Plausibility /6 | Max_disp /12 |
| ---------------- | --------------- | ------------ |
| Gemini 2.5 Flash | 2               | 3            |
| Gemini 3.1 Pro   | 1               | 3            |
| Claude Sonnet 5  | 0               | 7            |
| Claude Opus 4.8  | 0               | 10           |

Table 2: Standard sum of the scores for each aforementioned flags. Scores sum to a maximum total of 6 (tier 3 runs only) or 12 (tier 2 or 3 runs considered). The Gemini models showed more affluence in considering the plausibility of the roe deer, while the Claude models showed far more capability when addressing the maximum displacement issues.

**Means of Each Model**

| Model            | Blind (T1)  | Informed (T2) | False-label (T3) | Δ (T2 − T1)  | Δ / error |
| ---------------- | ----------- | ------------- | ---------------- | ------------ | --------- |
| Gemini 2.5 Flash | 6.67 ± 1.53 | 7.00 ± 1.00   | 6.33 ± 0.58      | +0.33 ± 1.05 | +0.32     |
| Gemini 3.1 Pro   | 7.00 ± 1.00 | 7.00 ± 0.00   | 7.67 ± 0.58      | +0.00 ± 0.58 | 0.00      |
| Claude Sonnet 5  | 8.67 ± 0.58 | 7.33 ± 0.58   | 8.33 ± 1.15      | −1.33 ± 0.47 | −2.83     |
| Claude Opus 4.8  | 9.00 ± 1.00 | 10.33 ± 1.15  | 9.00 ± 2.00      | +1.33 ± 0.88 | +1.51     |

Table 3: Means and standard deviation for each parameter are given. Headline number is calculated and error is given in its own column. The Claude models are clearly the most affected with Sonnet even scoring worse with informed data. With a test of n=3, the result is somewhat uninformative.

##### 6. Current Limitations:
- Claude does not allow sampling parameters to be set on the models chosen. Gemini uses default parameters for symmetry but this may not be the same as Claude's default.
- Thinking is set on for all models as Gemini's Pro model does not have the option to turn it off. Thinking also differs between dynamic (Gemini) and adaptive (Claude). 
- Claude models are routed via OpenRouter rather than Anthropic's API, because the Anthropic Console organisation was deleted and support could not restore access in time. The provider is pinned to Anthropic with fallbacks disabled and the resolved provider logged per run, so the requests are served on Anthropic infrastructure - but the billing and request path differ from Gemini, which uses the vendor API directly.
- The Flash pilot ran on Google's free tier, where prompts and responses may be used to improve Google's products. Later runs on the paid tier generally are not. So data handling differs between pilot and final batches.
- Three runs per model per tier is a small sample for a between-tier difference.
- Scoring is done by the person designing the test. Adding a second person would strengthen the result.
- The blind tier differs from the other two in more than framing - it also uses a different CSV, with neutralised column names, unit IDs, and relative periods. So blind versus informed confounds framing with column-name semantics.
- The false-label tier depends on the assumption that a competent reader should find 40–60 km displacements implausible for roe deer. That assumption is well founded but is itself a premise of the design rather than something the data tests.
- Model versions are moving targets. Gemini 3.1 Pro Preview is a preview identifier subject to renaming and behavioural change, so results are tied to the collection date rather than to a stable model.
- Hit three distinct Gemini failure modes in one morning: permanent quota restriction, empty responses, and server overload. The first two come hand in hand while the last is an issue on Google's behalf. Simple fixes (max tokens from 16000->32000 and waited 15 minutes then tried again on Google's side) but limitations nonetheless.
- In regard to billing, Opus blind runs ran more expensive than framed runs due to reasoning token billing.