import 'package:flutter/material.dart';
import 'package:wasteagram/screens/detail_screen.dart';
import 'package:wasteagram/screens/new_post_screen.dart';
import 'screens/list_screen.dart';

class App extends StatelessWidget {
  const App({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CS492 Project5',
      theme: ThemeData(brightness: Brightness.dark),
      routes: {
        ListScreen.routeName: (context) => const ListScreen(),
        DetailScreen.routeName: (context) => const DetailScreen(),
        NewPostScreen.routeName: (context) => const NewPostScreen()
      }
    );
  }
}