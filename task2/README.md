# Data submission

## Workflow

```diff
- Please read this section carefully before you start recording
```

1. Install the Android or iOS app (find in the GitLab repo), grant all permissions <u>before</u> starting the app
   * Can ask Matchy to help for Android installation
2. Wear the Lilygo band on the designated part of your body (and make sure it' on)
3. Open the Lilygo app, click "**start scan**"
4. A list of devices reachable from Bluetooth will appear, click the one named "**T-wristband**" and wait for the connection to be established (in Android app there the title of the plot will become "Receiving data")
5. Click "**Start Recording**". The app will prompt you to rename the json file. Recommended to rename it to: `lilygo_p<path_num>_<location>_<activity>.json`. For example: `lilygo_p0_wrist_justwalk.json`.
   * The activity here is the "anticipated" activity you're going to do. If you introduce additional activity like standing still or running, please rename the trace after you finish recording. The "**Note**" field in the app is *not* very useful because the full recording file will be several MBs large and it's hard to find the note in the middle of the file.
6. Walk and stop the recording after you reach the destination. The file will be saved to **Download** folder in Android, if you didn't change the default setting.
7. Use the script `trace_postproc.py` to process the raw trace file for submission. It will directly modify the trace file and perform data integrity check.

   ```bash
   # Usage
   python trace_postproc.py -f <trace_name>
   ```

8. Rename the processed trace as described in [Mandatory submission](#mandatory-submission) (e.g. `group24_trace<number>.json`).
9. Upload it to [our team's task2 dataset in Kaggle](https://www.kaggle.com/datasets/matchy/mham-task2-submission) and update [Mandatory submission](#mandatory-submission) table with an emoji indicating the recording is finished.
10. For additional submission, please update the list in [Additional submission](#additional-submission) and upload the trace to the same dataset.

## Path info

* Path 0: Central --  tram 10 -- HG
* Path 1: Central -- tram 10 -- Clausiusstrasse -- HG
* Path 2: Walchebrücke -- stairs -- tram 10 -- HG
* Path 3: Path 2 reversed
* Path 4: HG -- terrace stairs -- central -- Bahnhofquai (COOP)

## Mandatory submission

🐷 for posprocessed, ✅ for submitted.

| Pos \ Path  | 0      | 1      | 2      | 3      | 4      |
| ----------- | ------ | ------ | ------ | ------ | ------ |
| left wrist  | ✅`01`  | ✅`02`  | ✅ `03` | ✅`04`  | ✅ `05` |
| belt        | ✅`06`  | ✅`07`  | ✅`08`  | ✅`09`  | ✅`10`  |
| right ankle | ✅ `11` | ✅ `12` | ✅ `13` | ✅ `14` | ✅ `15` |

## Additional submission

Currently only have a placeholder showing the format. Please update the list as you submit additional traces.

* `16`: (location), (path), (activity), (posprocessed?/submitted?)
