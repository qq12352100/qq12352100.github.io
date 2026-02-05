import cv2
import numpy as np
import os

def find_similar_in_image(template_path, target_image_path, output_path='result.jpg'):
    """
    在单张目标图中查找与模板形状相似的位置，并用红色框标记
    
    :param template_path: 模板图片路径 (e.g., 'E://template.png')
    :param target_image_path: 目标图片路径 (e.g., 'E://1.jpg')
    :param output_path: 输出标记后的图片路径
    """
    # 1. 加载图像
    template = cv2.imread(template_path)
    target = cv2.imread(target_image_path)
    
    if template is None or target is None:
        raise FileNotFoundError("模板或目标图片加载失败，请检查路径")
    
    # 2. 转为灰度（特征检测需要）
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    
    # 3. 初始化ORB特征检测器（增加特征点数量，提高精度）
    orb = cv2.ORB_create(nfeatures=2000, edgeThreshold=30)
    
    # 4. 提取特征点和描述子
    kp1, des1 = orb.detectAndCompute(template_gray, None)
    kp2, des2 = orb.detectAndCompute(target_gray, None)
    
    if des1 is None or des2 is None:
        raise ValueError("无法提取特征点（模板或目标图可能是纯色/无纹理）")
    
    # 5. 使用 BFMatcher 替代 FLANN（避免兼容性问题）
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    matches = bf.knnMatch(des1, des2, k=2)
    
    # 6. Lowe's Ratio Test（过滤掉不好的匹配）
    good_matches = []
    for m, n in matches:
        if m.distance < 0.5 * n.distance:
            good_matches.append(m)
    
    # 7. 检查匹配点数量（至少需要4个点才能计算单应性）
    if len(good_matches) < 4:
        print(f"⚠️ 匹配点太少（{len(good_matches)} < 4），无法计算位置")
        print("建议：1. 降低阈值 2. 检查模板是否有纹理")
        cv2.imwrite(output_path, target)  # 直接输出原图
        return
    
    # 8. 获取匹配点坐标
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    
    # 9. 计算单应性矩阵（RANSAC过滤异常点）
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    
    if M is None:
        print("❌ 无法计算单应性矩阵（可能匹配点分布不合理）")
        cv2.imwrite(output_path, target)
        return
    
    # 10. 获取模板的四个角点
    h, w = template.shape[:2]
    pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
    
    # 11. 将角点投影到目标图
    dst = cv2.perspectiveTransform(pts, M)
    
    # 12. 在目标图上绘制红色框（四边形）
    img_result = target.copy()
    img_result = cv2.polylines(img_result, [np.int32(dst)], True, (0, 0, 255), 3)
    
    # 13. 保存结果
    cv2.imwrite(output_path, img_result)
    
    # 14. 显示结果（可选）
    cv2.namedWindow('Similar Match', cv2.WINDOW_NORMAL)
    cv2.imshow('Similar Match', img_result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print(f"✅ 匹配成功！结果已保存至: {os.path.abspath(output_path)}")
    return img_result

# =============== 使用示例 ===============
if __name__ == "__main__":
    # 配置路径（按需修改）
    TEMPLATE_PATH = 'E://Temp//template2.png'   # 模板图片
    TARGET_IMAGE_PATH = 'E://Temp//1.jpg'      # 目标图片
    
    find_similar_in_image(TEMPLATE_PATH, TARGET_IMAGE_PATH)