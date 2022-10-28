import 'package:flutter/material.dart';
import '../models/post_data.dart';

class PostDetail extends StatefulWidget {
  final PostData post;

  const PostDetail({Key? key, required this.post}) : super(key: key);

  @override
  State<PostDetail> createState() => _PostDetailState();
}

class _PostDetailState extends State<PostDetail> {
  Image? image;

  @override
  void initState() {
    super.initState();
    getImage();
  }

  void getImage() {
    image = Image.network(
      widget.post.imgUrl!, 
      loadingBuilder: ((context, child, loadingProgress) {
        if (loadingProgress == null) {
          return child;
        } else {
          return const Center(child: CircularProgressIndicator());
        }
    }));
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20),
      child: Center(
        child: Column(
          children: [
            Text(
              widget.post.convertDateToString(),
              style: const TextStyle(fontSize: 20),
            ),
            Padding(
              padding: const EdgeInsets.only(top: 10.0, bottom: 20.0),
              child: image!,
            ),
            Text(
              '${widget.post.quantity} Item(s)',
              style: const TextStyle(fontSize: 20),
            ),
            Padding(
              padding: const EdgeInsets.only(top: 40),
              child: Text(
                'Location: (${widget.post.latitude}, ${widget.post.longitude})',
                style: const TextStyle(fontSize: 18),
              ),
            )
          ],
        ),
      ),
    );
  }
}