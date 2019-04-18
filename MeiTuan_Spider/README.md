# MeiTuan-Spider
<hr/>

#### 说明:
- 抓取美团的美食版块，可以指定抓取的城市或抓取美团页面上的所有城市

#### 安装依赖包:
```python
pip install -r requirements.txt
```
#### 运行
```python
python main.py

# 或者使用以下方法
cd food
python food_module.py
```
#### 使用方法
- 如果需要抓取全部城市的美食版块信息， 只需要进入`food/food_module.py`模块中实现以下操作:
```python
all_data = True
```
- 默认为抓取单个城市的美食信息
