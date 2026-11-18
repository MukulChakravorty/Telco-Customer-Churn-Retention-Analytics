# DS-01: Telco Customer Churn & Retention Analytics

## Test Results and Model Evaluation

**Project:** Telco Customer Churn & Retention Analytics\
**Primary model:** LightGBM Churn Classifier\
**Supporting models:** KMeans Customer Segmentation, T-Learner Uplift
Model

> This report records values visible in the supplied project screenshots
> and previously reported application checks. Metrics have not been
> independently recomputed, and tests were not rerun specifically for
> this document.

## 1. Dataset and Data Quality

  Check                                                Observed result
  ------------------------------------------ -------------------------
  Dataset shape                                7,043 rows × 50 columns
  PostgreSQL data load                                      Successful
  Duplicate rows                                                     0
  Missing values in most displayed columns                           0
  `Churn Category` missing values                                5,174
  `Churn Reason` missing values                                  5,174

The two churn-detail columns have 5,174 missing values each. These
fields are associated with churned customers; their missingness should
be interpreted in context rather than automatically treated as a
data-cleaning failure.

## 2. Exploratory Data Analysis Highlights

### Churn distribution

  Churn label      Share
  ------------- --------
  No              73.46%
  Yes             26.54%

### Churn rate by customer characteristics

  Characteristic          Observed churn rate
  --------------------- ---------------------
  Age: Under 30                        22.37%
  Age: 30--45                          23.52%
  Age: 46--60                          24.31%
  Age: 60+                             36.46%
  Senior Citizen: No                   23.61%
  Senior Citizen: Yes                  41.68%
  Married: No                          32.96%
  Married: Yes                         19.66%
  Dependents: No                       32.55%
  Dependents: Yes                       6.52%

The displayed EDA results show higher churn among customers aged 60+,
senior citizens, unmarried customers, and customers without dependents.

### Tenure distribution

  Tenure group      Customer count
  --------------- ----------------
  0--6 months                1,470
  7--12 months                 716
  13--24 months              1,024
  25--48 months              1,594
  49--72 months              2,239

The 49--72 month group has the largest customer count; the 7--12 month
group has the smallest.

## 3. LightGBM Churn Classification

### Overall metrics

  Metric                           Result
  ------------------------------ --------
  Accuracy                         0.8510
  Precision                        0.7547
  Recall                           0.6497
  F1-score                         0.6983
  ROC-AUC                          0.9133
  Average Precision (PR curve)     0.7867

### Classification report

  Class                Precision   Recall   F1-score   Support
  ------------------ ----------- -------- ---------- ---------
  0 -- No Churn             0.88     0.92       0.90     1,035
  1 -- Churn                0.75     0.65       0.70       374
  Macro average             0.82     0.79       0.80     1,409
  Weighted average          0.85     0.85       0.85     1,409

### Confusion matrix

  Actual  Predicted     No Churn   Churn
  ------------------- ---------- -------
  No Churn                   956      79
  Churn                      131     243

-   True negatives: 956
-   False positives: 79
-   False negatives: 131
-   True positives: 243

The model correctly identifies many non-churning customers. It
identifies 243 churn customers, but misses 131 actual churn customers at
the displayed classification threshold. Churn-class recall is therefore
an improvement area.

### ROC and precision-recall curves

-   ROC-AUC: **0.9133**
-   Average Precision: **0.7867**

These curves provide additional views of discrimination and the
precision-recall trade-off.

## 4. KMeans Customer Segmentation

### Cluster-count comparison

    K       Inertia   Silhouette score
  --- ------------- ------------------
    2   34,306.3427             0.1853
    3   28,466.9194             0.2040
    4   24,647.6218             0.2006
    5   22,513.9279             0.1916
    6   20,860.7607             0.1914
    7   19,500.7415             0.1941
    8   18,309.4727             0.1951

The highest silhouette score among the tested values is **0.2040 at
K=3**. The elbow and silhouette outputs support K=3 as the selected
candidate among K=2 to K=8.

The silhouette score is relatively low, suggesting that the clusters are
not strongly separated. Segment-level business interpretation should
therefore be cautious.

## 5. T-Learner Uplift Model

### Displayed evaluation outputs

  Metric/output                                    Displayed result
  ---------------------------------------------- ------------------
  AUUC score (one evaluation output)                         0.7836
  Qini score (one evaluation output)                         0.2609
  AUUC (separate evaluation table)                           0.3747
  Qini coefficient (separate evaluation table)              -0.1275

### Targeting analysis

  -----------------------------------------------------------------------------------
  Targeting %   Customers     Control   Treatment    Control   Treatment    Displayed
                 selected   customers   customers churn rate  churn rate   difference
                                                                                 (pp)
  ----------- ----------- ----------- ----------- ---------- ----------- ------------
          10%         131          81          50     44.44%      36.00%        -8.44

          20%         263         151         112     41.72%      32.14%        -9.58

          30%         395         221         174     42.99%      35.63%        -7.35
  -----------------------------------------------------------------------------------

The table shows lower observed churn rates in the treatment group than
in the control group at these three targeting cut-offs.

### Validation caveat

The supplied outputs conflict: - AUUC and Qini values differ between the
standalone evaluation output and the separate evaluation table. - The
targeting-analysis narrative says the treatment group had a higher
observed churn rate for the top 10% and 20%, while the displayed table
shows lower treatment churn rates and negative treatment-minus-control
differences.

These outputs must not be combined into one definitive uplift claim. The
original calculation definitions, evaluation split, and sign convention
should be checked before making a final uplift-performance claim or
using it to justify campaign targeting. The project's displayed
conclusion also says the uplift model requires further refinement and
validation before it can support retention-campaign decisions.

## 6. Application and Integration Checks

The prior project walkthrough reported successful PostgreSQL data
loading and successful operation of the four deployed Streamlit modules:

  Component                 Previously observed status
  ------------------------- ----------------------------------------
  PostgreSQL dataset load   Successful; 7,043 × 50 shape displayed
  Business Overview         Working in prior live-app check
  Churn Analysis            Working in prior live-app check
  Customer Segmentation     Working in prior live-app check
  Retention ROI Simulator   Working in prior live-app check

These statuses are recorded from the earlier walkthrough; this document
does not represent a new automated test run.

## 7. Overall Test Summary

  -----------------------------------------------------------------------
  Area                                Summary
  ----------------------------------- -----------------------------------
  Dataset integrity                   7,043 rows, 50 columns; zero
                                      duplicate rows displayed

  Churn distribution                  26.54% churn; 73.46% non-churn

  LightGBM classifier                 ROC-AUC 0.9133; churn-class recall
                                      0.6497

  KMeans                              Highest tested silhouette score
                                      0.2040 at K=3

  T-Learner uplift                    Conflicting outputs require
                                      reconciliation; further validation
                                      needed

  Streamlit application               Four modules previously reported
                                      working

  PostgreSQL integration              Dataset load previously shown
                                      successful
  -----------------------------------------------------------------------

## 8. Conclusion

The project demonstrates a customer churn analytics workflow combining
data validation, exploratory analysis, churn classification, customer
segmentation, uplift modelling, database integration, and a Streamlit
dashboard.

The LightGBM model achieved a displayed ROC-AUC of 0.9133. Churn-class
recall of 0.6497 indicates that some churn customers are still missed
and that threshold selection or further model refinement may be useful.
KMeans selected K=3 among the tested cluster counts, although the
silhouette score indicates limited cluster separation. The uplift-model
outputs are inconsistent across the supplied results, so the model
should be treated as exploratory until those calculations are
reconciled.
