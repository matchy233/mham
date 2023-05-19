# Group 24 MHAM Report

**Team member**: Chong Zhang (22-945-562, `chozhang@student.ethz.ch`), Minghang Li (22-952-293, `minghli@student.ethz.ch`), Changsheng Li (22-944-474, `changli@student.ethz.ch`).

## Step Count

We employed conventional signal processing methods to quantify the number of steps. Initially, we computed the norm of the accelerations and/or angular velocities, which are the outputs of the gyroscope. The operations performed on these two time series were identical, though certain specific numerical values varied.

For the resulting norm series, we computed the signal envelope via a moving window maximum operation. This envelope was then subjected to a band-pass filter to eliminate the bias from low-frequency components and the noise from high-frequency components. Post filtering, we retained only the positive components of the signal and identified the peaks. Each identified peak corresponded to a single step. Finally, we attributed distinct weights to the results derived from acceleration and those derived from the gyroscope.

## Watch Location Detection

An initial review of relevant literature revealed that most algorithms utilize either Decision Trees or Support Vector Machines (SVMs) to achieve satisfactory classification results. Predominantly, they employ the time and frequency domain features of the accelerometer. Taking into consideration factors such as implementation difficulty, the methodology proposed in [1] and [2] was selected. Feature extraction was performed using the methods outlined by [2]:

The accelerometer data was first transformed into l2-norm (signal magnitude vector $SM = \sqrt{acc_x^2 + acc_y^2 + acc_z^2}$) and then partitioned into 10-second non-overlapping segments (jumping window). For **each window**, the following features were calculated: 1.The **mean** (feature 1) and **standard deviation** (feature 2) of the SM; 2. The **total power** in the frequencies between 0.3Hz and 15Hz (feature 3); 3. The **first and second dominant frequencies** (features 4 and 5) and their **powers** (features 6 and 7) in the frequencies between 0.3Hz and 15Hz; 4. The **dominant frequency** (feature 8) and its **power** (feature 9) in the frequencies between 0.6Hz and 2.5Hz; 5. The ratio between the power of the first dominant frequency and the total power (0.3 - 15Hz) (feature 10); 6. The ratio between the dominant frequencies listed in 3 and 4 of the current window and the previous window (feature 11, 12); 7. The ratio （R1） between the power at frequencies lower than 3 Hz and the total power (0.3 - 15 Hz) (feature 13); 8. The ratio （R2） between the power at frequencies higher than 3 Hz and the total power (0.3 - 15 Hz) (feature 14)

Upon completing the feature computation, as per the original paper, location detection solely requires the use of walking windows. Therefore, during both the training and prediction stages, we aggressively eliminated all windows suspected to be stationary based on the standard deviation of the feature vector. We retained only those windows that were assuredly associated with walking or cycling.

For a given trace, we executed predictions for each walking window, and the prediction that occurred most frequently was selected as the final prediction result for that trace.

The model was implemented using the Decision Tree (CART) in `scikit-learn`, which is very similar to C4.5 described in [1], if not better. To prevent overfitting, we imposed constraints on parameters like `max_depth` and `max_leaf_nodes`, etc.

## Activity Recognition

Given that feature extraction is a time-consuming process, we opted to implement the method proposed by [3] (originating from the same team as [2]) to repurpose the feature vector. We continued to use the 10-second windows and decision tree. However, the difference lies in the training process, where each window required a label. For this purpose, we selected traces from `trace.labels['activities']` that involved only a single activity for training, and each window was labeled as this activity during training. In this way, we can utilize this model to predict the activity for each window.

Notably, the prediction of the "standing still" activity, similar to step count, is rule-based and is independent of the prediction of other activities—since the occurrence of non-moving windows offers no benefit in predicting other activities. Similar to watch location detection, we aggressively discard all non-moving windows when predicting other activities before applying model prediction. Ultimately, for each trace, we consider an activity that appears more than `cont_thresh` times as an activity present within that trace.

## Path Index Detection

We incorporate both IMU (Inertial Measurement Unit) data and altitude data as features in our model.

Altitude data undergo a preprocessing stage where they are subjected to a low-pass filter, followed by normalization to a range between 0 and 1, after clipping any noisy values. Each sample is then divided into five sections, and the median value of each section is returned as the altitude features.

Regarding the IMU data, we employ the Madgwick filter to establish the orientation of the watch and subsequently obtain the relative yaw angle from the starting point. The sine and cosine values of these yaw angles are calculated and then subjected to a low-pass filter. These filtered values are divided into ten sections, and the median value of each section is extracted.

Consequently, the total number of features amounts to 25: 5 from the altitude data, 10 from the estimated yaw sine values, and 10 from the estimated yaw cosine values. These features are utilized to train a random forest classifier. Hyperparameters are tuned via 5-fold cross-validation.

## Reference

[1] K. Kunze, P. Lukowicz, H. Junker, and Gerhard Tröster, “Where am I: Recognizing On-body Positions of Wearable Sensors,” pp. 264–275, May 2005, doi: https://doi.org/10.1007/11426646_25.

[2] A. Mannini, A. M. Sabatini, and S. S. Intille, “Accelerometry-based recognition of the placement sites of a wearable sensor,” Pervasive and Mobile Computing, vol. 21, pp. 62–74, Aug. 2015, doi: https://doi.org/10.1016/j.pmcj.2015.06.003.

[3] A. Mannini, S. S. Intille, M. Rosenberger, A. M. Sabatini, and W. Haskell, “Activity Recognition Using a Single Accelerometer Placed at the Wrist or Ankle,” Medicine & Science in Sports & Exercise, vol. 45, no. 11, pp. 2193–2203, Nov. 2013, doi: https://doi.org/10.1249/mss.0b013e31829736d6.
