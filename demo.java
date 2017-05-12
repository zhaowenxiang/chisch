package com.letvcloud.sdk;


public class demo {
	
	public static void main(String[] args) throws Exception {
        String USER_UNIQUE = "用户唯一标识码";
        String SECRET_KEY = "分配的秘钥";
        LetvCloudV1 client = new LetvCloudV1(USER_UNIQUE, SECRET_KEY);
  
        //定义输出格式 (json|xml)
        client.format = "xml";

        //视频上传初始化（Web方式）
        String response = client.videoUploadInit("乐视云视频");
        System.out.println(response);         
        //视频上传（Web方式）
        String response2 = client.videoUpload("C:/Documents and Settings/Administrator/桌面/kara.mp4","http://123.456.789.012/api/fileupload?offset=0&token=aaabbbccc&fmt=xml");
        System.out.println(response2); 
        //视频上传（Flash方式）
        String response3 = client.videoUploadFlash("乐视云视频", "", 600, 450, "10.10.80.153");
        System.out.println(response3); 
        
        //获取单个视频信息
        int videoid = 4139137;
        String response4 = client.videoGet(videoid);
        System.out.println(response4); 
        //编辑单个视频的相关信息
        String response5 = client.videoUpdate(videoid, "abc", "desc", "tag", 0);
        System.out.println(response5); 
        
        //获取HTML代码播放地址
        String response6 = client.videoGetPlayinterface("abcde12345","a1b2c3d4f5","html", "", -1, 960, 480);
        System.out.println(response6);         

        //获取以天为单位的所有数据
        String response7 = client.dataTotalDate("2012-10-01", "2013-06-01", 1, 20);       
        System.out.println(response7);
          
	}
}
