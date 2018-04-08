import wx
from math import pi


class CalculatorFrame(wx.Frame):
    def __init__(self, title):
        super(CalculatorFrame, self).__init__(None, title=title, pos=(300, 300), size=(300, 250))

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        # BoxSizer用于布局管理
        # 水平方向：wx.VERTICAL    垂直方向：wx.HORIZONTAL
        vbox = wx.BoxSizer(wx.VERTICAL)
        # style是文本的对齐方式
        self.textprint = wx.TextCtrl(self, -1, '', style=wx.TE_RIGHT | wx.TE_READONLY)
        # 用于存储文本内容
        self.equation = ""
        # wx.EXPAND: 项目将扩大，以填补提供给它的空间(wx.GROW是一样的)。border是组件周围的像素空间
        vbox.Add(self.textprint, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=4)
        # 创建5行4列的网格，水平和垂直间距都是5
        gridBox = wx.GridSizer(5, 4, 5, 5)
        # labels = ['AC', 'DEL', 'pi', 'CLOSE', '7', '8', '9', '/', '4', '5', '6',
        #           '*', '1', '2', '3', '-', '0', '.', '=', '+']
        labels = ['AC', 'DEL', '(', ')', '7', '8', '9', '/', '4', '5', '6',
                  '*', '1', '2', '3', '-', '0', '.', '=', '+']
        # 向网格中添加按钮
        for label in labels:
            buttonItem = wx.Button(self, label=label)
            self.createHandler(buttonItem, label)
            gridBox.Add(buttonItem, 1, wx.EXPAND)
        # proportion: 控件所在方向上占的空间相对于其他组件的比例，只对boxsizer有意义。0为保持本身大小，1占1/3，2占2/3；flag表示组件的对齐方式、边框有无、是否扩展、是否拉伸等等
        vbox.Add(gridBox, proportion=1, flag=wx.EXPAND)
        # 在父中创建的子窗口必须被添加给sizer，sizer管理每个窗口部件的尺寸和位置
        self.SetSizer(vbox)

    def createHandler(self, button, labels):
        item = "DEL AC = CLOSE"
        if labels not in item:
            # 绑定事件
            self.Bind(wx.EVT_BUTTON, self.OnAppend, button)
        elif labels == 'DEL':
            self.Bind(wx.EVT_BUTTON, self.OnDel, button)
        elif labels == 'AC':
            self.Bind(wx.EVT_BUTTON, self.OnAc, button)
        elif labels == '=':
            self.Bind(wx.EVT_BUTTON, self.OnTarget, button)
        elif labels == 'CLOSE':
            self.Bind(wx.EVT_BUTTON, self.OnExit, button)

    def OnAppend(self, event):
        # 获取事件对象
        eventbutton = event.GetEventObject()
        # 获取对象的Label值
        label = eventbutton.GetLabel()
        self.equation += label
        # 设置TextCtrl控件中的值
        self.textprint.SetValue(self.equation)

    def OnDel(self, event):
        # 删除最后一个字符
        self.equation = self.equation[:-1]
        self.textprint.SetValue(self.equation)

    def OnAc(self, event):
        # 清零
        self.textprint.Clear()
        self.equation = ""

    def OnTarget(self, event):
        string = self.equation
        try:
            # eval函数的功能：将字符串str当成有效的表达式来求值并返回计算结果
            target = eval(string)
            self.equation = str(target)
            self.textprint.SetValue(self.equation)
        except SyntaxError:
            dlg = wx.MessageDialog(self, u'格式错误，请输入正确的等式!',
                                   u'请注意', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def OnExit(self, event):
        self.Close()


if __name__ == "__main__":
    app = wx.App()
    CalculatorFrame("calculator")
    app.MainLoop()
