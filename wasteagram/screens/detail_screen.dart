import 'package:flutter/material.dart';
import '../models/post_data.dart';
import '../components/post_detail.dart';

class DetailScreen extends StatefulWidget {
  static const routeName = '/detail';
  const DetailScreen({Key? key}) : super(key: key);

  @override
  State<DetailScreen> createState() => _DetailScreenState();
}

class _DetailScreenState extends State<DetailScreen> {
  @override
  Widget build(BuildContext context) {
    final post = ModalRoute.of(context)!.settings.arguments as PostData;

    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: const Text('Wasteagram', style: TextStyle(fontSize: 25))
      ),
      body: PostDetail(post: post)
    );
  }
}