import 'dart:io';
import 'package:flutter/material.dart';
import 'package:location/location.dart';
import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_storage/firebase_storage.dart';

class NewPostForm extends StatefulWidget {
  const NewPostForm({Key? key}) : super(key: key);

  @override
  State<NewPostForm> createState() => _NewPostFormState();
}

class _NewPostFormState extends State<NewPostForm> {
  LocationData? locationData;
  var locationService = Location();
  File? image;
  String? imgUrl;
  final picker = ImagePicker();
  int? wastedCount;
  final _formKey = GlobalKey<FormState>();

  @override
  void initState() {
    super.initState();
    retrieveLocation();
    getImage();
  }

  void retrieveLocation() async {
    try {
      var serviceEnabled = await locationService.serviceEnabled();
      if (!serviceEnabled) {
        serviceEnabled = await locationService.requestService();
        if (!serviceEnabled) {
          print('Failed to enable service. Returning.');
          return;
        }
      }

      var permissionGranted = await locationService.hasPermission();
      if (permissionGranted == PermissionStatus.denied) {
        permissionGranted = await locationService.requestPermission();
        if (permissionGranted != PermissionStatus.granted) {
          print('Location service permission not granted. Returning.');
        }
      }
      
      locationData = await locationService.getLocation();
    } on PlatformException catch (e) {
      print('Error: ${e.toString()}, code: ${e.code}');
      locationData = null;
    }
    locationData = await locationService.getLocation();
    setState(() {});
  }

  void getImage() async {
    final pickedFile = await picker.pickImage(source: ImageSource.gallery);
    image = File(pickedFile!.path);
    setState(() {});
  } 

  Future storeImage() async {
    final String fileName = '${DateTime.now().toString()}.jpg';
    Reference storageReference = FirebaseStorage.instance.ref().child(fileName);
    UploadTask uploadTask = storageReference.putFile(image!);
    await uploadTask;
    final url = await storageReference.getDownloadURL();
    return url;
  }

  Future uploadPostData() async {
    imgUrl = await storeImage();
    FirebaseFirestore.instance.collection("wasteagram_posts").add({
      'quantity': wastedCount,
      'latitude': locationData!.latitude,
      'longitude': locationData!.longitude,
      'imgUrl': imgUrl,
      'dateTime':Timestamp.fromDate(DateTime.now())
    });
  }

  @override
  Widget build(BuildContext context) {
    if (image == null) {
      return const Center(child: CircularProgressIndicator());
    } else {
      return SingleChildScrollView(
        child: Column(
          children: [
            selectedImg(),
            formGenerator(),
            const SizedBox(height: 40),
            uploadButton(context)
          ]
        ),
      );
    }
  }

  Widget selectedImg() {
  return Padding(
      padding: const EdgeInsets.all(10.0),
      child: Image.file(image!),
    );
  }

  Widget formGenerator() {
    return Form(
      key:_formKey,
      child: Semantics(
        enabled: true,
        onTapHint: "Please enter the number of wasted items",
        child: Padding(
          padding: const EdgeInsets.only(left: 10.0, right: 10.0, bottom: 10.0),
          child: TextFormField(
            autofocus: false,
            textAlign: TextAlign.center,
            style: const TextStyle(fontSize: 25.0, height: 2.0),
            decoration: const InputDecoration(
              labelText: "Number of Wasted Items", border: UnderlineInputBorder()
            ),
            keyboardType: TextInputType.number,
            onSaved: (value) => wastedCount = int.parse(value!),
            validator: (value){
              if (value == null || value.isEmpty) {
                return 'Please Enter Number of Items.';
              } else {
                return null;
              }
            }
          ),
        )
      ) 
    );
  }

  Widget uploadButton(BuildContext context) {
    return Semantics(
      button: true,
      enabled: true,
      onTapHint: 'Save the post',
      child: ElevatedButton(
        child: const Icon(Icons.cloud_upload, size:80),
        onPressed: () async {
          if (_formKey.currentState!.validate()) {
            _formKey.currentState!.save();
            await uploadPostData();
            Navigator.of(context).pop(true);
          }
        },
      )
    );
  }
}