import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'new_post_screen.dart';
import 'detail_screen.dart';
import '../models/list_posts.dart';

class ListScreen extends StatefulWidget {
  static const routeName = '/';
  const ListScreen({Key? key}) : super(key: key);

  @override
  State<ListScreen> createState() => _ListScreenState();
}

class _ListScreenState extends State<ListScreen> {
  final listPosts = ListPosts();
  num? totalWastedCount;

  @override
  void initState() {
    super.initState();
    setTotalWastedCount();
  }

  void setTotalWastedCount() async {
    num count = 0;
    var snapshot = await FirebaseFirestore.instance.collection('wasteagram_posts').get();
    for (var element in snapshot.docs) {
      count += element['quantity'];
    }
    totalWastedCount = count;
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: Text(
          'Wasteagram - $totalWastedCount', 
          style: const TextStyle(fontSize: 25)
        )
      ),
      body: postList(context),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerDocked,
      floatingActionButton: Semantics(
        button: true,
        enabled: true,
        onTapHint: 'Select an image',
        child: cameraFab()
      ),
    );
  }

  Widget cameraFab() {
    return Padding(
      padding: const EdgeInsets.all(10.0),
      child: SizedBox(
        height: 70,
        width: 70,
        child: FloatingActionButton(
          child: const Icon(Icons.camera_alt, size:40),
          onPressed: () {
            Navigator.of(context).pushNamed(NewPostScreen.routeName);
          }
        ),
      ),
    );
  }

  Widget postList(BuildContext context){
    return StreamBuilder(
      stream: FirebaseFirestore.instance.collection('wasteagram_posts').snapshots(),
      builder: (BuildContext context, AsyncSnapshot<QuerySnapshot> snapshot) {
        if (snapshot.hasData && snapshot.data!.docs.isNotEmpty) {
          listPosts.addPostsToList(snapshot);
          listPosts.sortPostsByDate();
          return ListView.builder(
            itemCount: listPosts.posts.length,
            itemBuilder: (context, index) {
              var post = listPosts.posts[index];
              return Semantics(
                enabled: true,
                onTapHint: "Check ${post.convertDateToString()}'s post. Wasted ${post.quantity} Items",
                child: ListTile(
                  title: Text(
                    post.convertDateToString(), 
                    style: const TextStyle(fontSize: 20)
                  ),
                  trailing: Text(
                    post.quantity.toString(),
                    style: const TextStyle(fontSize: 20)
                  ),
                  onTap: (){
                    Navigator.of(context).pushNamed(
                      DetailScreen.routeName,
                      arguments: post
                    );
                  }
                )
              );
            },
          );
        } else {
          return const Center(child: CircularProgressIndicator());
        }
      }
    );
  }

}