import 'package:intl/intl.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

class PostData {
  int? quantity;
  String? latitude;
  String? longitude;
  String? imgUrl;
  DateTime? dateTime;

  PostData({
    required this.quantity,
    required this.latitude,
    required this.longitude,
    required this.imgUrl,
    required this.dateTime
  });

  String convertDateToString() {
    return DateFormat.yMMMEd().format(dateTime!).toString();
  }

  PostData.fromSnapshot(DocumentSnapshot snapshot) :
    quantity = snapshot['quantity'],
    latitude = snapshot['latitude'].toString(),
    longitude = snapshot['longitude'].toString(),
    imgUrl = snapshot['imgUrl'],
    dateTime = snapshot['dateTime'].toDate();
  
  PostData.fromMap(Map post) :
    quantity = post['quantity'],
    latitude = post['latitude'],
    longitude = post['longitude'],
    imgUrl = post['imgUrl'],
    dateTime = post['dateTime'];
}