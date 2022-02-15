# FaceMaskRecognition
Using Yolov5 for face mask detection, we use our own dataset to detect if someone is wearing a mask properly.
We aim to detect 3 classes:
- Mask: the mask is correctly wore
- BadMask: the mask is not correctly wore
- NoMask: no mask is wore

This project was led by three student at ISEN: **Victor GAYA, Cyril DELANNOY, Arnaud FRANCOISE**

## Dataset description
* First we used a kaggle dataset to improve our model.
* Then we created our dataset by filming and anoting videos


## Results
![alt text](https://github.com/goldentrex/FaceMaskRecognition/blob/9ddcd6c0c31113d2182c95d7ec3d88270d78387f/Demo/democapture.png)

From the confusion matrix  we can say that our model has successfully learned how to recognise whether a person wear a mask or not (chirurgical mask precisely). However we can see that it struggles to identify when the mask is not wore correctly.
This is not supprising considering the data on which the model was trained. There is less annotated files with the class "BadMask". To improve that we could run a data augmentation process or just acquire new data from this class.
![alt text](https://github.com/goldentrex/FaceMaskRecognition/blob/8448a80c6aca3981e1dbb151463fa288b41dfe3a/Demo/confusionmatrix.png)

Another bias is the ethnicity. Indeed our algorithm was trained mainly on images representing white people, it has not sufficiantly learn to recognise people from other ethnic
To go further it could be interesting to improve the dataset with different type of mask

This is the repartition of the classes in the dataset we made ourselves, we can see that most of the classes are related to Mask and NoMask.
As we said earlier to push this project one step further we need to improve the dataset on several point: 

*   More data with the BadMask class
*   More diversity in ethnicity
*   More diveristy in the type of mask

