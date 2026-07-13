# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox

class JiangSuanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("匠算 v0.0.1 - 清式古建筑无斗拱大木作木构件计算器")
        # 加上下面这行代码，即可改变软件左上角和任务栏的图标
        try:
            self.root.iconbitmap('logo.ico')
        except Exception:
            pass # 如果文件丢失，程序也能正常启动而不会报错崩溃
        self.root.geometry("780x640")
        self.root.minsize(700, 550)
        
        # 配置整体主题与样式
        self.setup_styles()
        
        # 绘制主界面布局
        self.create_widgets()
        
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # 配置框架和元素
        self.style.configure("TFrame", background="#F7F5F0")
        self.style.configure("Header.TFrame", background="#3A322D")
        self.style.configure("Card.TFrame", background="#FFFFFF", relief="solid", borderwidth=1)
        
        # 标签样式
        self.style.configure("TLabel", background="#F7F5F0", foreground="#333333", font=("Helvetica", 10))
        self.style.configure("HeaderTitle.TLabel", background="#3A322D", foreground="#EAE2B7", font=("Helvetica", 14, "bold"))
        self.style.configure("HeaderSub.TLabel", background="#3A322D", foreground="#DDA15E", font=("Helvetica", 9, "italic"))
        self.style.configure("Section.TLabel", background="#FFFFFF", foreground="#3A322D", font=("Helvetica", 11, "bold"))
        self.style.configure("CardLabel.TLabel", background="#FFFFFF", font=("Helvetica", 10))
        
        # 按钮样式（朱砂红）
        self.style.configure("Action.TButton", background="#8B261E", foreground="#FFFFFF", font=("Helvetica", 10, "bold"), padding=6)
        self.style.map("Action.TButton", background=[("active", "#A63A32"), ("pressed", "#701E17")])
        
        # 下拉框
        self.style.configure("TCombobox", padding=4)
        
    def create_widgets(self):
        # 1. 顶部标头
        header_frame = ttk.Frame(self.root, style="Header.TFrame", padding=(15, 10))
        header_frame.pack(side="top", fill="x")
        
        title_label = ttk.Label(header_frame, text="匠 算  v0.0.1", style="HeaderTitle.TLabel")
        title_label.pack(anchor="w")
        sub_label = ttk.Label(header_frame, text="清式古建筑小式无斗拱·举高与步架通用精确计算工具 (暂不支持六/八檩卷棚)", style="HeaderSub.TLabel")
        sub_label.pack(anchor="w", pady=(2, 0))
        
        # 主主体框架
        body_frame = ttk.Frame(self.root, padding=15)
        body_frame.pack(side="top", fill="both", expand=True)
        
        # 左侧参数面板
        left_panel = ttk.Frame(body_frame, width=320, padding=(0, 0, 10, 0))
        left_panel.pack(side="left", fill="both")
        left_panel.pack_propagate(False)
        
        # 右侧结果面板
        right_panel = ttk.Frame(body_frame)
        right_panel.pack(side="right", fill="both", expand=True)
        
        # --- 左侧：参数录入卡片 ---
        input_card = ttk.Frame(left_panel, style="Card.TFrame", padding=15)
        input_card.pack(fill="both", expand=True)
        
        ttk.Label(input_card, text="〖 参数录入 (单位: mm) 〗", style="Section.TLabel").pack(anchor="w", pady=(0, 12))
        
        # 檩条数量选择
        ttk.Label(input_card, text="1. 选定檩条数量 (根):", style="CardLabel.TLabel").pack(anchor="w", pady=(4, 2))
        self.puris_var = tk.StringVar()
        self.puris_combo = ttk.Combobox(input_card, textvariable=self.puris_var, values=["3", "4", "5", "7", "9"], state="readonly")
        self.puris_combo.pack(fill="x", pady=(0, 10))
        self.puris_combo.current(2) # 默认5檩
        self.puris_combo.bind("<<ComboboxSelected>>", self.on_puris_change)
        
        # 通进深输入
        ttk.Label(input_card, text="2. 测量通进深 (mm):", style="CardLabel.TLabel").pack(anchor="w", pady=(4, 2))
        self.depth_entry = ttk.Entry(input_card, font=("Helvetica", 10))
        self.depth_entry.insert(0, "6000") # 默认示例值改 mm
        self.depth_entry.pack(fill="x", pady=(0, 10))
        
        # 动态条件输入框容器
        self.dynamic_frame = ttk.Frame(input_card, style="Card.TFrame")
        self.dynamic_frame.pack(fill="x", pady=(5, 10))
        
        # 动态输入控件初始化
        self.extra_entry = ttk.Entry(self.dynamic_frame, font=("Helvetica", 10))
        
        # 根据默认选择初始化可见性
        self.on_puris_change()
        
        # 计算按钮
        calc_btn = ttk.Button(input_card, text="开始匠心精密计算", style="Action.TButton", command=self.perform_calculations)
        calc_btn.pack(fill="x", side="bottom", pady=(10, 0))
        
        # --- 右侧：精算结果报表 ---
        result_card = ttk.Frame(right_panel, style="Card.TFrame", padding=15)
        result_card.pack(fill="both", expand=True)
        
        ttk.Label(result_card, text="〖 精算结果报表 (单位: mm) 〗", style="Section.TLabel").pack(anchor="w", pady=(0, 10))
        
        # 带滚动条的文本控制台
        text_scroll = ttk.Scrollbar(result_card)
        text_scroll.pack(side="right", fill="y")
        
        self.result_text = tk.Text(result_card, wrap="word", yscrollcommand=text_scroll.set, 
                                   font=("Consolas", 11), bg="#FAFAFA", fg="#2B2B2B", relief="flat", padx=8, pady=8)
        self.result_text.pack(side="left", fill="both", expand=True)
        text_scroll.config(command=self.result_text.yview)
        
        self.log_text(">> 系统就绪。请在左侧设定大木作实测数据(mm)，然后点击计算。\n")

def on_puris_change(self, event=None):

    # 删除旧控件
    for widget in self.dynamic_frame.winfo_children():
        widget.destroy()

    p_count = self.puris_var.get()

    if p_count in ("4", "9"):
        # 有额外输入时显示
        self.dynamic_frame.pack(fill="x", pady=(5, 10))

        if p_count == "4":
            ttk.Label(
                self.dynamic_frame,
                text="3. 四架梁两端檐檩中线尺寸 (mm):",
                style="CardLabel.TLabel"
            ).pack(anchor="w", pady=(2,2))

            self.extra_entry = ttk.Entry(self.dynamic_frame)
            self.extra_entry.insert(0,"4800")
            self.extra_entry.pack(fill="x")

        elif p_count == "9":
            ttk.Label(
                self.dynamic_frame,
                text="3. 实测檐柱径大小 (mm):",
                style="CardLabel.TLabel"
            ).pack(anchor="w", pady=(2,2))

            self.extra_entry = ttk.Entry(self.dynamic_frame)
            self.extra_entry.insert(0,"400")
            self.extra_entry.pack(fill="x")

    else:
        # 3、5、7檩直接隐藏整个Frame
        self.dynamic_frame.pack_forget()

    def log_text(self, text, clear=False):
        self.result_text.config(state="normal")
        if clear:
            self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state="disabled")
        self.result_text.see(tk.END)

    def perform_calculations(self):
        try:
            depth = float(self.depth_entry.get())
            puris = int(self.puris_var.get())
        except ValueError:
            messagebox.showerror("输入非法", "通进深和规格基础必须是合法的数字！")
            return
            
        if depth <= 0:
            messagebox.showerror("数据不合实际", "通进深必须为大于零的正数。")
            return
            
        extra_val = 0.0
        if puris in [4, 9]:
            try:
                extra_val = float(self.extra_entry.get())
                if extra_val <= 0: raise ValueError
            except ValueError:
                field_name = "檐檩中线尺寸" if puris == 4 else "檐柱径"
                messagebox.showerror("输入非法", f"请输入正确的正数：【{field_name}】")
                return

        # 核心古建筑数学推算
        step_count = (puris - 1) / 2
        avg_step = (depth / 2) / step_count if step_count > 0 else 0
        
        # 格式化报告文本（全修改为 .2f 毫米输出）
        out = []
        out.append("┌────────────────────────────────────────────────────────┐")
        out.append(f"  匠算大木作分析报告 —— 建筑形制：{puris}檩题案")
        out.append("└────────────────────────────────────────────────────────┘")
        out.append(f"• 实测通进深总量: {depth:.2f} mm")
        out.append(f"• 理论单面均分步架数量: {step_count} 架")
        out.append(f"• 基础均分单步架跨度: {avg_step:.2f} mm")
        out.append("─" * 56)
        
        if puris == 3:
            out.append("【三檩小式结构详情】")
            out.append(f"  » 檐/脊步架尺寸 = {avg_step:.2f} mm")
            out.append("  » 脊檩举高弹性推荐选型（依据传统营造法则调整）：")
            out.append(f"    - 方案一 (平缓·五举): {avg_step * 0.5:.2f} mm")
            out.append(f"    - 方案二 (标准·七举): {avg_step * 0.7:.2f} mm")
            out.append(f"    - 方案三 (陡峻·八举): {avg_step * 0.8:.2f} mm")
            
        elif puris == 4:
            out.append("【四檩小式卷棚结构详情】")
            out.append(f"  » 实测两端檐檩中线尺寸: {extra_val:.2f} mm")
            out.append(f"  » 顶步架尺寸 (中线1/5): {extra_val / 5:.2f} mm  [建议在2-3倍柱径范围内微调]")
            out.append(f"  » 檐步架尺寸 (中线2/5): {2 * (extra_val / 5):.2f} mm")
            out.append("  » 脊举高弹性推荐选择:")
            out.append(f"    - 方案一 (五举系数): {avg_step * 0.5:.2f} mm")
            out.append(f"    - 方案二 (七举系数): {avg_step * 0.7:.2f} mm")
            out.append(f"    - 方案三 (八举系数): {avg_step * 0.8:.2f} mm")
            
        elif puris == 5:
            out.append("【五檩小式结构详情】")
            out.append(f"  » 檐步架跨度 = 金步架跨度 = {avg_step:.2f} mm")
            out.append(f"  » 金檩位置举高 (按五举): {avg_step * 0.5:.2f} mm")
            out.append(f"  » 脊檩位置举高 (按七举): {avg_step * 0.7:.2f} mm")
            
        elif puris == 7:
            out.append("【七檩小式结构详情 (多重传统举架解法方案推荐)】")
            out.append(f"  » 基础步架跨度 (檐步=金步=脊步): {avg_step:.2f} mm")
            schemes = [
                ("方案一 (传统平缓式 - 5举/7举/6.5举)", [0.5, 0.7, 0.65]),
                ("方案二 (规整通用式 - 5举/65举/8举)", [0.5, 0.65, 0.8]),
                ("方案三 (北方陡峻式 - 5举/65举/85举)", [0.5, 0.65, 0.85])
            ]
            for s_name, coefs in schemes:
                out.append(f"  * {s_name}:")
                out.append(f"    - 檐举高尺寸: {avg_step * coefs[0]:.2f} mm")
                out.append(f"    - 金举高尺寸: {avg_step * coefs[1]:.2f} mm")
                out.append(f"    - 脊举高尺寸: {avg_step * coefs[2]:.2f} mm")
                
        elif puris == 9:
            out.append("【九檩大式结构详情 (依规矩根据柱径模数扩展)】")
            out.append(f"  » 实测檐柱径大小: {extra_val:.2f} mm")
            
            # 方案一：4倍柱径
            es1 = 4 * extra_val
            out.append(f"  * 方案一 (檐步架按 4倍檐柱径 = {es1:.2f} mm)：")
            out.append(f"    - 下金步架 = 上金步架 = 脊步架 = {avg_step:.2f} mm")
            out.append(f"    - 檐举高: {es1 * 0.5:.2f} mm | 下金举: {avg_step * 0.65:.2f} mm")
            out.append(f"    - 上金举: {avg_step * 0.75:.2f} mm | 脊举高: {avg_step * 0.9:.2f} mm")
            
            # 方案二：5倍柱径
            es2 = 5 * extra_val
            out.append(f"  * 方案二 (檐步架按 5倍檐柱径 = {es2:.2f} mm)：")
            out.append(f"    - 下金步架 = 上金步架 = 脊步架 = {avg_step:.2f} mm")
            out.append(f"    - 檐举高: {es2 * 0.5:.2f} mm | 下金举: {avg_step * 0.65:.2f} mm")
            out.append(f"    - 上金举: {avg_step * 0.75:.2f} mm | 脊举高: {avg_step * 0.9:.2f} mm")

        out.append("\n>> 计算完毕。数据仅供修缮及大木营造参考。")
        self.log_text("\n".join(out), clear=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = JiangSuanApp(root)
    root.mainloop()