package com.utils;

import okhttp3.*;
import org.json.JSONObject;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.Base64;
import java.util.concurrent.TimeUnit;

public class FaceUtil {

    public static final String API_KEY = "ql21uVftf13jXL0FGEkFCCzH";
    public static final String SECRET_KEY = "81L7L2FRTMcEkuMr3opuyx8cccXsEw20";

    public static final OkHttpClient HTTP_CLIENT = new OkHttpClient().newBuilder().readTimeout(300, TimeUnit.SECONDS).build();

    public static void registerFace(String base64Image, String userId) throws IOException {

        // 假设的 group_id 和 user_id，你可以根据实际情况修改
        String groupId = "aabb";

        MediaType mediaType = MediaType.parse("application/json");
        // 使用 Base64 编码替换请求体中的 "BASE64"，并添加 group_id 和 user_id
        RequestBody body = RequestBody.create(mediaType, "{\"image_type\":\"BASE64\",\"image\":\"" + base64Image + "\",\"group_id\":\"" + groupId + "\",\"user_id\":\"" + userId + "\"}");
        Request request = new Request.Builder()
                .url("https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add?access_token=" + getAccessToken())
                .method("POST", body)
                .addHeader("Content-Type", "application/json")
                .build();
        Response response = HTTP_CLIENT.newCall(request).execute();
        System.out.println(response.body().string());
    }
    public static String findFace(String base64Image) throws IOException {
        // 假设的 group_id_list，你可以根据实际情况修改
        String[] groupIdList = {"aabb"};
        String groupIdListStr = String.join("\",\"", groupIdList);

        MediaType mediaType = MediaType.parse("application/json");
        // 构建包含 image_type、image 和 group_id_list 的请求体
        RequestBody body = RequestBody.create(mediaType, "{\"image_type\":\"BASE64\",\"image\":\"" + base64Image + "\",\"group_id_list\":\"" + groupIdListStr + "\"}");
        Request request = new Request.Builder()
                .url("https://aip.baidubce.com/rest/2.0/face/v3/search?access_token=" + getAccessToken())
                .method("POST", body)
                .addHeader("Content-Type", "application/json")
                .build();
        Response response = HTTP_CLIENT.newCall(request).execute();
        String responseBody = response.body().string();
        System.out.println(responseBody);

        JSONObject jsonResponse = new JSONObject(responseBody);
        if (jsonResponse.has("result")) {
            JSONObject result = jsonResponse.getJSONObject("result");
            if (result.has("user_list")) {
                return result.getJSONArray("user_list").getJSONObject(0).getString("user_id");
            }
        }
        return null;
    }

    private static String encodeImageToBase64(String filePath) throws IOException {
        File file = new File(filePath);
        try (FileInputStream imageInFile = new FileInputStream(file)) {
            byte[] imageData = new byte[(int) file.length()];
            imageInFile.read(imageData);
            return Base64.getEncoder().encodeToString(imageData);
        }
    }


    /**
     * 从用户的AK，SK生成鉴权签名（Access Token）
     *
     * @return 鉴权签名（Access Token）
     * @throws IOException IO异常
     */
    static String getAccessToken() throws IOException {
        MediaType mediaType = MediaType.parse("application/x-www-form-urlencoded");
        RequestBody body = RequestBody.create(mediaType, "grant_type=client_credentials&client_id=" + API_KEY
                + "&client_secret=" + SECRET_KEY);
        Request request = new Request.Builder()
                .url("https://aip.baidubce.com/oauth/2.0/token")
                .method("POST", body)
                .addHeader("Content-Type", "application/x-www-form-urlencoded")
                .build();
        Response response = HTTP_CLIENT.newCall(request).execute();
        return new JSONObject(response.body().string()).getString("access_token");
    }
}
