"""
合约计算器 Android版本
使用Kivy框架开发的跨平台应用
"""

import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.text import LabelBase
from kivy.clock import Clock
import json
import os
from datetime import datetime
import platform

# 设置中文字体支持
FONT_NAME = "Chinese"

def setup_chinese_font():
    """设置中文字体"""
    # Windows系统的常见中文字体
    font_files = [
        'C:/Windows/Fonts/msyh.ttc',  # 微软雅黑
        'C:/Windows/Fonts/simhei.ttf',  # 黑体
        'C:/Windows/Fonts/simsun.ttc',  # 宋体
    ]
    
    for font_path in font_files:
        if os.path.exists(font_path):
            try:
                LabelBase.register(name=FONT_NAME, fn_regular=font_path)
                print(f"注册字体成功: {font_path}")
                return
            except Exception as e:
                print(f"注册字体失败: {font_path}, 错误: {e}")
                continue
    
    print("未找到合适的中文字体，将使用默认字体")

# 初始化字体
setup_chinese_font()

class ChineseLabel(Label):
    """支持中文的Label"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = FONT_NAME

class ChineseButton(Button):
    """支持中文的Button"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = FONT_NAME

class ContractScreen(Screen):
    """合约计算器主界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'contract'
        self.build_ui()
    
    def build_ui(self):
        """构建UI"""
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title = ChineseLabel(
            text='📊 合约计算器',
            font_size=20,
            size_hint_y=None,
            height=40
        )
        main_layout.add_widget(title)
        
        # 输入区域
        input_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=200)
        
        # 开仓价格
        input_layout.add_widget(ChineseLabel(text='开仓价格:', font_size=14))
        self.open_price = TextInput(
            text='',
            multiline=False,
            input_filter='float',
            font_name=FONT_NAME
        )
        input_layout.add_widget(self.open_price)
        
        # 现价
        input_layout.add_widget(ChineseLabel(text='现价:', font_size=14))
        self.current_price = TextInput(
            text='',
            multiline=False,
            input_filter='float',
            font_name=FONT_NAME
        )
        input_layout.add_widget(self.current_price)
        
        # 杠杆倍数
        input_layout.add_widget(ChineseLabel(text='杠杆倍数:', font_size=14))
        self.leverage = TextInput(
            text='',
            multiline=False,
            input_filter='float',
            font_name=FONT_NAME
        )
        input_layout.add_widget(self.leverage)
        
        # 本金
        input_layout.add_widget(ChineseLabel(text='本金:', font_size=14))
        self.principal = TextInput(
            text='',
            multiline=False,
            input_filter='float',
            font_name=FONT_NAME
        )
        input_layout.add_widget(self.principal)
        
        main_layout.add_widget(input_layout)
        
        # 计算按钮
        calc_btn = ChineseButton(
            text='💰 计算',
            size_hint_y=None,
            height=50,
            font_size=16
        )
        calc_btn.bind(on_press=self.calculate)
        main_layout.add_widget(calc_btn)
        
        # 结果显示区域
        result_layout = BoxLayout(orientation='vertical', spacing=10)
        
        self.percent_change_label = ChineseLabel(
            text='📊 现货涨幅: 0.00%',
            font_size=14,
            size_hint_y=None,
            height=30
        )
        result_layout.add_widget(self.percent_change_label)
        
        self.reverse_change_label = ChineseLabel(
            text='📉 现货跌幅: 0.00%',
            font_size=14,
            size_hint_y=None,
            height=30
        )
        result_layout.add_widget(self.reverse_change_label)
        
        self.profit_loss_label = ChineseLabel(
            text='💸 盈亏: ¥0.00',
            font_size=16,
            size_hint_y=None,
            height=35
        )
        result_layout.add_widget(self.profit_loss_label)
        
        self.total_label = ChineseLabel(
            text='💰 总计: ¥0.00',
            font_size=16,
            size_hint_y=None,
            height=35
        )
        result_layout.add_widget(self.total_label)
        
        main_layout.add_widget(result_layout)
        
        # 底部按钮
        bottom_layout = BoxLayout(spacing=10, size_hint_y=None, height=50)
        
        calc_button = ChineseButton(text='🔢 计算器')
        calc_button.bind(on_press=self.goto_calculator)
        bottom_layout.add_widget(calc_button)
        
        compound_button = ChineseButton(text='📈 复利')
        compound_button.bind(on_press=self.goto_compound)
        bottom_layout.add_widget(compound_button)
        
        main_layout.add_widget(bottom_layout)
        
        self.add_widget(main_layout)
    
    def calculate(self, *args):
        """计算合约盈亏"""
        try:
            open_price = float(self.open_price.text or 0)
            current_price = float(self.current_price.text or 0)
            leverage = float(self.leverage.text or 1)
            principal = float(self.principal.text or 0)
            
            if open_price <= 0 or current_price <= 0:
                return
            
            # 计算涨跌幅
            percent_change = ((current_price - open_price) / open_price) * 100
            reverse_change = -percent_change
            
            # 计算盈亏
            profit_loss = principal * (percent_change / 100) * leverage
            total = principal + profit_loss
            
            # 更新显示
            self.percent_change_label.text = f'📊 现货涨幅: {percent_change:.2f}%'
            self.reverse_change_label.text = f'📉 现货跌幅: {reverse_change:.2f}%'
            self.profit_loss_label.text = f'💸 盈亏: ¥{profit_loss:.2f}'
            self.total_label.text = f'💰 总计: ¥{total:.2f}'
            
        except ValueError:
            pass
    
    def goto_calculator(self, *args):
        """跳转到计算器"""
        self.manager.current = 'calculator'
    
    def goto_compound(self, *args):
        """跳转到复利计算器"""
        self.manager.current = 'compound'

class CalculatorScreen(Screen):
    """计算器界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'calculator'
        self.calc_input = ""
        self.calc_storage = []
        self.calc_just_calculated = False
        self.calc_data_file = None
        self.build_ui()
        self.load_calc_storage()
    
    def build_ui(self):
        """构建计算器UI"""
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题和返回按钮
        header = BoxLayout(size_hint_y=None, height=40, spacing=10)
        
        back_btn = ChineseButton(text='← 返回', size_hint_x=None, width=80)
        back_btn.bind(on_press=self.go_back)
        header.add_widget(back_btn)
        
        title = ChineseLabel(text='🔢 计算器', font_size=18)
        header.add_widget(title)
        
        main_layout.add_widget(header)
        
        # 显示屏
        self.calc_display = TextInput(
            text='0',
            readonly=True,
            multiline=False,
            font_size=20,
            size_hint_y=None,
            height=50,
            font_name=FONT_NAME
        )
        main_layout.add_widget(self.calc_display)
        
        # 按钮区域
        buttons_layout = GridLayout(cols=4, spacing=5)
        
        # 按钮布局：存储、清空、退格、÷
        button_layout = [
            ['存储', '清空', '退格', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['清除存储', '0', '.', '=']
        ]
        
        for row in button_layout:
            for btn_text in row:
                btn = ChineseButton(text=btn_text, font_size=14)
                btn.bind(on_press=lambda x, text=btn_text: self.calc_button_click(text))
                buttons_layout.add_widget(btn)
        
        main_layout.add_widget(buttons_layout)
        
        # 存储记录显示
        storage_label = ChineseLabel(
            text='💾 存储记录:',
            size_hint_y=None,
            height=30,
            font_size=14
        )
        main_layout.add_widget(storage_label)
        
        # 存储记录列表
        scroll = ScrollView(size_hint_y=0.3)
        self.calc_storage_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.calc_storage_layout.bind(minimum_height=self.calc_storage_layout.setter('height'))
        scroll.add_widget(self.calc_storage_layout)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def calc_button_click(self, button_text):
        """处理计算器按钮点击"""
        if button_text in '0123456789.':
            if self.calc_just_calculated:
                self.calc_input = button_text
                self.calc_just_calculated = False
            else:
                if self.calc_input == '0' or self.calc_input == '':
                    self.calc_input = button_text
                else:
                    self.calc_input += button_text
        
        elif button_text in ['+', '-', '×', '÷']:
            self.calc_just_calculated = False
            if self.calc_input and self.calc_input[-1] not in ['+', '-', '×', '÷']:
                self.calc_input += button_text
        
        elif button_text == '=':
            if self.calc_input:
                try:
                    # 替换显示符号为Python计算符号
                    calc_string = self.calc_input.replace('×', '*').replace('÷', '/')
                    result = eval(calc_string)
                    
                    # 存储记录
                    record = f"{self.calc_input} → {result}"
                    if record not in self.calc_storage:
                        self.calc_storage.append(record)
                        self.save_calc_storage()
                        self.update_calc_storage_display()
                    
                    self.calc_input = str(result)
                    self.calc_just_calculated = True
                    
                except Exception:
                    self.calc_input = "错误"
                    self.calc_just_calculated = True
        
        elif button_text == '清空':
            self.calc_input = '0'
            self.calc_just_calculated = False
        
        elif button_text == '退格':
            self.calc_just_calculated = False
            if len(self.calc_input) > 1:
                self.calc_input = self.calc_input[:-1]
            else:
                self.calc_input = '0'
        
        elif button_text == '存储':
            if self.calc_input and self.calc_input != '0':
                record = f"存储: {self.calc_input}"
                if record not in self.calc_storage:
                    self.calc_storage.append(record)
                    self.save_calc_storage()
                    self.update_calc_storage_display()
        
        elif button_text == '清除存储':
            self.calc_storage.clear()
            self.save_calc_storage()
            self.update_calc_storage_display()
        
        # 更新显示
        self.calc_display.text = self.calc_input if self.calc_input else '0'
    
    def update_calc_storage_display(self):
        """更新存储记录显示"""
        self.calc_storage_layout.clear_widgets()
        
        for i, record in enumerate(reversed(self.calc_storage[-10:])):  # 显示最近10条
            record_layout = BoxLayout(size_hint_y=None, height=30, spacing=5)
            
            record_label = ChineseLabel(
                text=record,
                font_size=12,
                size_hint_x=0.8
            )
            record_layout.add_widget(record_label)
            
            copy_btn = ChineseButton(
                text='复制',
                size_hint_x=0.2,
                font_size=10
            )
            copy_btn.bind(on_press=lambda x, r=record: self.copy_to_calc_display(r))
            record_layout.add_widget(copy_btn)
            
            self.calc_storage_layout.add_widget(record_layout)
    
    def copy_to_calc_display(self, record):
        """复制记录到显示屏"""
        if " → " in record:
            result = record.split(" → ")[1]
            self.calc_input = result
            self.calc_display.text = result
            self.calc_just_calculated = False
        elif "存储: " in record:
            value = record.replace("存储: ", "")
            self.calc_input = value
            self.calc_display.text = value
            self.calc_just_calculated = False
    
    def load_calc_storage(self):
        """加载计算器存储记录"""
        if self.calc_data_file and os.path.exists(self.calc_data_file):
            try:
                with open(self.calc_data_file, 'r', encoding='utf-8') as f:
                    self.calc_storage = json.load(f)
                self.update_calc_storage_display()
            except Exception as e:
                print(f"加载计算器数据失败: {e}")
                self.calc_storage = []
    
    def save_calc_storage(self):
        """保存计算器存储记录"""
        if self.calc_data_file:
            try:
                os.makedirs(os.path.dirname(self.calc_data_file), exist_ok=True)
                with open(self.calc_data_file, 'w', encoding='utf-8') as f:
                    json.dump(self.calc_storage, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"保存计算器数据失败: {e}")
    
    def go_back(self, *args):
        """返回主界面"""
        self.manager.current = 'contract'

class CompoundScreen(Screen):
    """复利计算器界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'compound'
        self.compound_records = []
        self.compound_total = 0
        self.data_file = None
        self.build_ui()
        self.load_data()
    
    def build_ui(self):
        """构建复利计算器UI"""
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题和返回按钮
        header = BoxLayout(size_hint_y=None, height=40, spacing=10)
        
        back_btn = ChineseButton(text='← 返回', size_hint_x=None, width=80)
        back_btn.bind(on_press=self.go_back)
        header.add_widget(back_btn)
        
        title = ChineseLabel(text='📈 复利计算器', font_size=18)
        header.add_widget(title)
        
        main_layout.add_widget(header)
        
        # 输入区域
        input_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=100)
        
        input_layout.add_widget(ChineseLabel(text='今日收益:', font_size=14))
        self.profit_input = TextInput(
            text='',
            multiline=False,
            input_filter='float',
            font_name=FONT_NAME
        )
        input_layout.add_widget(self.profit_input)
        
        input_layout.add_widget(ChineseLabel(text='本金重置:', font_size=14))
        self.reset_input = TextInput(
            text='',
            multiline=False,
            input_filter='float',
            font_name=FONT_NAME
        )
        input_layout.add_widget(self.reset_input)
        
        main_layout.add_widget(input_layout)
        
        # 操作按钮
        btn_layout = BoxLayout(spacing=10, size_hint_y=None, height=50)
        
        add_btn = ChineseButton(text='➕ 添加收益')
        add_btn.bind(on_press=self.add_profit)
        btn_layout.add_widget(add_btn)
        
        reset_btn = ChineseButton(text='🔄 重置本金')
        reset_btn.bind(on_press=self.reset_principal)
        btn_layout.add_widget(reset_btn)
        
        main_layout.add_widget(btn_layout)
        
        # 总计显示
        self.total_label = ChineseLabel(
            text=f'💰 当前总计: ¥{self.compound_total:.2f}',
            font_size=16,
            size_hint_y=None,
            height=40
        )
        main_layout.add_widget(self.total_label)
        
        # 历史记录
        history_label = ChineseLabel(
            text='📊 收益历史:',
            size_hint_y=None,
            height=30,
            font_size=14
        )
        main_layout.add_widget(history_label)
        
        # 历史记录列表
        scroll = ScrollView()
        self.history_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        scroll.add_widget(self.history_layout)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
        self.update_history_display()
    
    def add_profit(self, *args):
        """添加收益"""
        try:
            profit = float(self.profit_input.text or 0)
            if profit != 0:
                now = datetime.now()
                record = {
                    'date': now.strftime('%m/%d'),
                    'time': now.strftime('%H:%M'),
                    'profit': profit,
                    'total_before': self.compound_total,
                    'total_after': self.compound_total + profit
                }
                
                self.compound_records.append(record)
                self.compound_total += profit
                
                self.profit_input.text = ''
                self.update_total_display()
                self.update_history_display()
                self.save_data()
                
        except ValueError:
            pass
    
    def reset_principal(self, *args):
        """重置本金"""
        try:
            new_principal = float(self.reset_input.text or 0)
            if new_principal >= 0:
                now = datetime.now()
                record = {
                    'date': now.strftime('%m/%d'),
                    'time': now.strftime('%H:%M'),
                    'profit': 0,
                    'total_before': self.compound_total,
                    'total_after': new_principal,
                    'reset': True
                }
                
                self.compound_records.append(record)
                self.compound_total = new_principal
                
                self.reset_input.text = ''
                self.update_total_display()
                self.update_history_display()
                self.save_data()
                
        except ValueError:
            pass
    
    def update_total_display(self):
        """更新总计显示"""
        self.total_label.text = f'💰 当前总计: ¥{self.compound_total:.2f}'
    
    def update_history_display(self):
        """更新历史记录显示"""
        self.history_layout.clear_widgets()
        
        for i, record in enumerate(reversed(self.compound_records[-20:])):  # 显示最近20条
            record_layout = BoxLayout(size_hint_y=None, height=40, spacing=5)
            
            if record.get('reset'):
                text = f"{record['date']} {record['time']} 重置: ¥{record['total_after']:.2f}"
            else:
                profit_text = f"+{record['profit']:.2f}" if record['profit'] >= 0 else f"{record['profit']:.2f}"
                text = f"{record['date']} {record['time']} {profit_text} → ¥{record['total_after']:.2f}"
            
            record_label = ChineseLabel(
                text=text,
                font_size=12,
                size_hint_x=0.6
            )
            record_layout.add_widget(record_label)
            
            edit_btn = ChineseButton(
                text='编辑',
                size_hint_x=0.2,
                font_size=10
            )
            edit_btn.bind(on_press=lambda x, idx=len(self.compound_records)-1-i: self.edit_record(idx))
            record_layout.add_widget(edit_btn)
            
            delete_btn = ChineseButton(
                text='删除',
                size_hint_x=0.2,
                font_size=10
            )
            delete_btn.bind(on_press=lambda x, idx=len(self.compound_records)-1-i: self.delete_record(idx))
            record_layout.add_widget(delete_btn)
            
            self.history_layout.add_widget(record_layout)
    
    def edit_record(self, index):
        """编辑记录"""
        if 0 <= index < len(self.compound_records):
            record = self.compound_records[index]
            # 这里可以添加编辑对话框，目前先删除再添加
            self.delete_record(index)
    
    def delete_record(self, index):
        """删除记录"""
        if 0 <= index < len(self.compound_records):
            self.compound_records.pop(index)
            self.recalculate_compound_total()
            self.update_total_display()
            self.update_history_display()
            self.save_data()
    
    def recalculate_compound_total(self):
        """重新计算复利总额"""
        self.compound_total = 0
        for i, record in enumerate(self.compound_records):
            if record.get('reset'):
                self.compound_total = record['total_after']
            else:
                self.compound_total += record['profit']
            # 更新记录中的总额
            record['total_before'] = self.compound_total - record.get('profit', 0)
            record['total_after'] = self.compound_total
    
    def load_data(self):
        """加载数据"""
        if self.data_file and os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.compound_records = data.get('records', [])
                    self.compound_total = data.get('total', 0)
                self.update_total_display()
                self.update_history_display()
            except Exception as e:
                print(f"加载数据失败: {e}")
                self.compound_records = []
                self.compound_total = 0
    
    def save_data(self):
        """保存数据"""
        if self.data_file:
            try:
                data = {
                    'records': self.compound_records,
                    'total': self.compound_total
                }
                os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
                with open(self.data_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"保存数据失败: {e}")
    
    def go_back(self, *args):
        """返回主界面"""
        self.manager.current = 'contract'

class CalculatorApp(App):
    """主应用"""
    
    def build(self):
        # 设置应用存储路径
        if platform.system() == 'Android':
            from android.storage import primary_external_storage_path
            app_storage_path = os.path.join(primary_external_storage_path(), 'Android', 'data', 'org.example.contractcalculator', 'files')
        else:
            app_storage_path = os.path.dirname(os.path.abspath(__file__))
        
        # 创建屏幕管理器
        sm = ScreenManager()
        
        # 创建屏幕
        contract_screen = ContractScreen()
        calculator_screen = CalculatorScreen()
        compound_screen = CompoundScreen()
        
        # 设置数据文件路径
        calculator_screen.calc_data_file = os.path.join(app_storage_path, 'calculator_data.json')
        compound_screen.data_file = os.path.join(app_storage_path, 'compound_data.json')
        
        # 重新加载数据
        calculator_screen.load_calc_storage()
        compound_screen.load_data()
        
        # 添加屏幕到管理器
        sm.add_widget(contract_screen)
        sm.add_widget(calculator_screen)
        sm.add_widget(compound_screen)
        
        return sm

if __name__ == '__main__':
    CalculatorApp().run()
