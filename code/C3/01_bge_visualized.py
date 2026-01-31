import torch
from visual_bge.visual_bge.modeling import Visualized_BGE

from pathlib import Path
SCRIPT_DIR = Path(__file__).resolve().parent
model = Visualized_BGE(model_name_bge="BAAI/bge-base-en-v1.5",
                      model_weight= SCRIPT_DIR / "../../models/bge/Visualized_base_en_v1.5.pth")
model.eval()

with torch.no_grad():
    text_emb = model.encode(text="datawhale开源组织的logo")
    img_emb_1 = model.encode(image=SCRIPT_DIR/"../../data/C3/imgs/datawhale01.png")
    multi_emb_1 = model.encode(image=SCRIPT_DIR/"../../data/C3/imgs/datawhale01.png", text="datawhale开源组织的logo")
    img_emb_2 = model.encode(image=SCRIPT_DIR/"../../data/C3/imgs/datawhale02.png")
    multi_emb_2 = model.encode(image=SCRIPT_DIR/"../../data/C3/imgs/datawhale02.png", text="datawhale开源组织的logo")

# 计算相似度
sim_1 = img_emb_1 @ img_emb_2.T
sim_2 = img_emb_1 @ multi_emb_1.T
sim_3 = text_emb @ multi_emb_1.T
sim_4 = multi_emb_1 @ multi_emb_2.T

print("=== 相似度计算结果 ===")
print(f"纯图像 vs 纯图像: {sim_1}")
print(f"图文结合1 vs 纯图像: {sim_2}")
print(f"图文结合1 vs 纯文本: {sim_3}")
print(f"图文结合1 vs 图文结合2: {sim_4}")

# 向量信息分析
print("\n=== 嵌入向量信息 ===")
print(f"多模态向量维度: {multi_emb_1.shape}")
print(f"图像向量维度: {img_emb_1.shape}")
print(f"多模态向量示例 (前10个元素): {multi_emb_1[0][:10]}")
print(f"图像向量示例 (前10个元素):   {img_emb_1[0][:10]}")


import requests
from PIL import Image
from io import BytesIO

def image_byteio_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return BytesIO(response.content)

img_dog = image_byteio_from_url(
            "https://cdn.britannica.com/16/234216-050-C66F8665/beagle-hound-dog.jpg")

img_dog2 = image_byteio_from_url("https://hips.hearstapps.com/hmg-prod/images/golden-retriever-puppy-lying-down-on-grass-royalty-free-image-1766098805.pjpeg?crop=1.00xw:0.754xh;0,0.136xh&resize=1400:*")
with torch.no_grad():
    eb_img_dog = model.encode(image=img_dog)
    eb_img_dog2 = model.encode(image=img_dog2)
    eb_mult_1 = model.encode(image=img_dog, text="这是一只狗")
    eb_mult_2 = model.encode(image=img_dog2, text="这是一只狗")
    eb_img_cat = model.encode(
        image=image_byteio_from_url("https://i.guim.co.uk/img/media/327aa3f0c3b8e40ab03b4ae80319064e401c6fbc/377_133_3542_2834/master/3542.jpg?width=620&dpr=2&s=none&crop=none"))

"""
图片相似度：狗1 vs 狗2: tensor([[0.6985]])
图片+文本相似度：狗1 vs 狗2: tensor([[0.8139]])
图片相似度：狗1 vs 猫: tensor([[0.6913]])
"""
print(f"图片相似度：狗1 vs 狗2: {eb_img_dog @ eb_img_dog2.T}")
print(f"图片+文本相似度：狗1 vs 狗2: {eb_mult_1 @ eb_mult_2.T}")
print(f"图片相似度：狗1 vs 猫: {eb_img_dog @ eb_img_cat.T}")