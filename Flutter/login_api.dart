import 'package:dio/dio.dart';

final response = await dio.post(
  "/login",
  data: {"username": user, "password": pass},
);

token = response.data["access_token"];