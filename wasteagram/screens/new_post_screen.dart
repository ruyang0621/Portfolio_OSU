import 'package:flutter/material.dart';
import '../components/new_post_form.dart';

class NewPostScreen extends StatelessWidget {
  static const routeName = '/new_post';
  const NewPostScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: const Text("Add New Post", style: TextStyle(fontSize: 25))
      ),
      body: const NewPostForm(),
    );
  }
}