import 'package:flutter/material.dart';
import 'post_data.dart';

class ListPosts {
  List<PostData> posts;
  ListPosts({List<PostData>? posts}) : posts = posts ?? [];

  void addPostsToList(AsyncSnapshot snapshot) {
    posts.clear();
    snapshot.data.docs.forEach((document){
      final post = PostData.fromSnapshot(document);
      posts.add(post);
    });
  }

  void sortPostsByDate() {
    posts.sort(((a, b) => b.dateTime!.compareTo(a.dateTime!)));
  }
}