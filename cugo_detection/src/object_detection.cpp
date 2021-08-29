#include "object_detection.h"

void ImageConverter::publishStr(cv::Point2f center, float radius)
{
        if( 0 <= center.x && center.x <= 240)
        {
                str.data = "turn left";
                msg_pub.publish(str);
                // ROS_INFO("turn left");
        }
        else if( 400 < center.x && center.x <= 640)
        {
                str.data = "turn right";
                msg_pub.publish(str);
                // ROS_INFO("turn right");
        }
        else
        {
                if(radius >= 130.0 || radius <= 10) {
                        str.data = "stop";
                        msg_pub.publish(str);
                        // ROS_INFO("stop");
                }
                else{
                        str.data = "go ahead";
                        msg_pub.publish(str);
                        // ROS_INFO("go ahead");
                }
        }
        // ROS_INFO("{x:%f, y:%f}", center.x, center.y);
        // ROS_INFO("size:%d", cv_ptr->image.size().width);
        // ROS_INFO("radius = %f", radius);
}

int ImageConverter::maxContours(std::vector<std::vector<cv::Point>> contours)
{
        double max_area = 0;
        int max_area_contour = -1;
        if(contours.size() > 0)
        {
                for(int j=0; j<contours.size(); j++) {
                        double area = cv::contourArea(contours.at(j));
                        if( max_area < area ) {
                                max_area = area;
                                max_area_contour=j;
                        }
                }
        }
        else
        {
                // ROS_INFO("target nothing!");
                str.data = "stop";
                msg_pub.publish(str);
        }
        if(max_area_contour == -1)
        {
                // ROS_INFO("target nothing( max_area )!");
                str.data = "stop";
                msg_pub.publish(str);
        }
        return(max_area_contour);
}

void ImageConverter::imageCb(const sensor_msgs::ImageConstPtr& msg)
{
        cv::Point2f center, p1;
        cv_bridge::CvImagePtr cv_ptr,cv_edge;
        float radius;
        nh_.getParam("/object_detection/hue_mn", hue_mn);
        nh_.getParam("/object_detection/hue_mx", hue_mx);
        nh_.getParam("/object_detection/sat_mn", sat_mn);
        nh_.getParam("/object_detection/sat_mx", sat_mx);
        nh_.getParam("/object_detection/value_mn", value_mn);
        nh_.getParam("/object_detection/value_mx", value_mx);
        nh_.getParam("/object_detection/bright_mn", bright_mn);
        nh_.getParam("/object_detection/bright_mx", bright_mx);

        try
        {       // ROSからOpenCVの形式にtoCvCopy()で変換。cv_ptr->imageがcv::Matフォーマット
                cv_ptr  = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
                cv_edge = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::MONO8);
        }catch(cv_bridge::Exception& e)
        {
                ROS_ERROR("cv_bridge exception: %s", e.what());
                return;
        }
        cv::Mat hsv_image, color_mask, gray_image, threshold_image, bit_image;
        // RGB表色系をHSV表色系へ変換して、hsv_imageに格納
        cv::cvtColor(cv_ptr->image, hsv_image, CV_BGR2HSV);

        // 色相(Hue), 彩度(Saturation), 明暗(Value, brightness)
        // 指定した範囲の色でマスク画像color_mask(CV_8U:符号なし8ビット整数)を生成
        cv::inRange(hsv_image, 
        cv::Scalar(hue_mn, sat_mn, value_mn, bright_mn) , cv::Scalar(hue_mx, sat_mx, value_mx, bright_mx),
        color_mask);  // 赤

        // ビット毎の論理積。マスク画像は指定した範囲以外は0で、指定範囲の要素は255なので、ビット毎の論理積を適用すると、指定した範囲の色に対応する要素はそのままで、他は0になる。
        cv::bitwise_and(cv_ptr->image, cv_ptr->image, bit_image, color_mask);
        // グレースケールに変換
        cv::cvtColor(bit_image, gray_image, CV_BGR2GRAY);
        // エッジを検出するためにCannyアルゴリズムを適用
        cv::Canny(gray_image, cv_edge->image, 15.0, 30.0, 3);
        // 閾値80で2値画像に変換
        cv::threshold(gray_image, threshold_image, 80, 255, CV_THRESH_BINARY);

        // ウインドウに円を描画
        //cv::circle(cv_ptr->image, cv::Point(100, 100), 20, CV_RGB(0,255,0));

        // 輪郭を格納するcontoursにfindContours関数に渡すと輪郭を点の集合として入れてくれる
        std::vector<std::vector<cv::Point>> contours;
        cv::findContours(threshold_image, contours, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_NONE);

        int max_area_contour = ImageConverter::maxContours(contours);

        // 最大面積を持つ輪郭の最小外接円を取得
        if(max_area_contour == -1) return;
        cv::minEnclosingCircle(contours.at(max_area_contour), center, radius);
        // 最小外接円を描画(画像、円の中心座標、半径、色、線の太さ)
        cv::circle(cv_ptr->image, center, radius, cv::Scalar(0,0,255),3,4);

        // 画面中心から最小外接円の中心へのベクトルを描画
        p1 = cv::Point2f(cv_ptr->image.size().width/2,cv_ptr->image.size().height/2);
        cv::arrowedLine(cv_ptr->image, p1, center, cv::Scalar(0, 255, 0, 0), 3, 8, 0, 0.1);

        // 画像サイズは縦横1/4に変更
        cv::Mat cv_half_image, cv_half_image2, cv_half_image3, cv_half_image4, cv_half_image5;
        cv::resize(cv_ptr->image, cv_half_image,cv::Size(),0.75,0.75);
        cv::resize(bit_image, cv_half_image2,cv::Size(),0.75,0.75);
        cv::resize(cv_edge->image, cv_half_image3,cv::Size(),0.75,0.75);
        cv::resize(threshold_image, cv_half_image5,cv::Size(),0.75,0.75);
        
        ImageConverter::publishStr(center, radius);

        cv::imshow("Original Image", cv_half_image);
        cv::imshow("Result Image", cv_half_image2);
        cv::drawContours(cv_ptr->image, contours, -1, cv::Scalar(255, 0, 0), 6);
        cv::imshow("threshold_image", cv_ptr->image);
        cv::waitKey(3);
}

int main(int argc, char** argv)
{
        ros::init(argc, argv, "object_detection");
        ImageConverter ic;
        ros::spin();
        return 0;
}
