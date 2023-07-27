# learner-handwriting-recognition

This repository comprises the Transcription Guidelines for Learner Handwritings while Retaining Orthographic Errors, the IAA-Analysis and the Converter as described in the paper _Preserving the Authenticity of Handwritten Learner Language: Annotation Guidelines for Creating Transcripts Retaining Orthographic Features_.

It further comprises the German Spelling Error Generator as described in _Recognizing Learner Handwriting Retaining Orthographic Errors for Enabling Fine-Grained Error Feedback_.

# Terms of Use & Citation
This research may be used for non-commercial research purposes only. If you publish material based on this database - please refer to the information in the following papers:

<br>

Christian Gold, Ronja Laarmann-Quante, Torsten Zesch. 2023. Preserving the Authenticity of Handwritten Learner Language: Annotation Guidelines for Creating Transcripts Retaining Orthographic Features. 1st Computation and Written Language (CAWL) Workshop at ACL.
[Link to Publication](https://aclanthology.org/2023.cawl-1.3/)
<br>

Christian Gold, Ronja Laarmann-Quante, Torsten Zesch. 2023. Recognizing Learner Handwriting Retaining Orthographic Errors for Enabling Fine-Grained Error Feedback. Innovative Use of NLP for Building Educational Applications (BEA) Workshop at ACL.
[Link to Publication](https://aclanthology.org/2023.bea-1.28/)


# Converter

You can test run the Converter_Transcript4HWR from console with: <br>
```python Converter_Transcript4HWR.py -i src/test_data.txt -o result/test_data_result_4HWR.txt```


You can test run the Converter_Transcript4ContinuousText from console with: <br>
```python Converter_Transcript4ContinuousText.py -i src/test_data.txt -o result/test_data_result_4ContinuousText.txt```
