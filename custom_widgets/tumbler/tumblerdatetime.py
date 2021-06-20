from PySide2.QtCore import Slot
from PySide2.QtWidgets import QWidget, QHBoxLayout
from tumbler import Tumbler


class TumblerDateTime(QWidget):
    """
    日期时间滑动选择器控件
    作者:feiyangqingyun(QQ:517216493) 2017-8-11
    译者:sunchuquin(QQ:1715216365) 2021-06-20
    1. 可设置年月日时分秒
    2. 可鼠标或者手指滑动选择年月日时分秒
    3. 支持自定义数值范围
    4. 支持鼠标滚轮选择
    5. 年月日自动联动计算
    """

    def __init__(self, parent: QWidget = None):
        super(TumblerDateTime, self).__init__(parent)
        self.__tumblerYear: Tumbler = Tumbler(self)  # 年份选择器
        self.__tumblerMonth: Tumbler = Tumbler(self)  # 月份选择器
        self.__tumblerDay: Tumbler = Tumbler(self)  # 日期选择器
        self.__tumblerHour: Tumbler = Tumbler(self)  # 时钟选择器
        self.__tumblerMin: Tumbler = Tumbler(self)  # 分钟选择器
        self.__tumblerSec: Tumbler = Tumbler(self)  # 秒钟选择器
        self.initForm()
    
    @Slot()
    def initForm(self) -> None:
        self.__tumblerYear.listValue = [str(i) for i in range(1900, 2101)]
        self.__tumblerMonth.listValue = [str(i) + ' 月' for i in range(1, 13)]
        self.__tumblerDay.listValue = [str(i) for i in range(1, 32)]
        self.__tumblerHour.listValue = [str(i) for i in range(0, 24)]
        self.__tumblerMin.listValue = [str(i) for i in range(0, 60)]
        self.__tumblerSec.listValue = [str(i) for i in range(0, 60)]
        # 年月日联动
        self.__tumblerYear.currentValueChanged.connect(self.currentValueChanged)
        self.__tumblerMonth.currentValueChanged.connect(self.currentValueChanged)

        # 将选择器添加到布局
        layout: QHBoxLayout = QHBoxLayout(self)
        layout.setMargin(0)
        layout.setSpacing(0)
        layout.addWidget(self.__tumblerYear)
        layout.addWidget(self.__tumblerMonth)
        layout.addWidget(self.__tumblerDay)
        layout.addWidget(self.__tumblerHour)
        layout.addWidget(self.__tumblerMin)
        layout.addWidget(self.__tumblerSec)

    @Slot()
    def currentValueChanged(self, value: str) -> None:
        month: int = int(self.__tumblerMonth.currentValue[:2])
        day: int = int(self.__tumblerDay.currentValue[:2])  # 记住之前的日期

        # 计算该月最大日期
        if month is 2:  # 平年28天 闰年29天
            year: int = int(self.__tumblerYear.currentValue[:4])
            isLoopYear: bool = (0 is (year % 4)) and (0 is not (year % 100)) or (0 is (year % 400))
            if isLoopYear: maxDay: int = 29
            else: maxDay: int = 28
        elif month in [1, 3, 5, 7, 8, 10, 12]: maxDay: int = 31
        else: maxDay: int = 30

        self.__tumblerDay.listValue = [str(i) for i in range(1, maxDay + 1)]

        # 如果上次的日期大于最大的日期则设置为最大的日期
        if day > maxDay: self.__tumblerDay.currentIndex = maxDay - 1
        else: self.__tumblerDay.currentIndex = day - 1
    
    @property
    def year(self) -> int: return int(self.__tumblerYear.currentValue)
    
    @year.setter
    def year(self, n_year: int) -> None: self.__tumblerYear.currentValue = str(n_year)
    
    @property
    def month(self) -> int: return int(self.__tumblerMonth.currentValue[:2])
    
    @month.setter
    def month(self, n_month: int) -> None: self.__tumblerMonth.currentValue = str(n_month) + ' 月'
    
    @property
    def day(self) -> int: return int(self.__tumblerDay.currentValue)
    
    @day.setter
    def day(self, n_day: int) -> None: self.__tumblerDay.currentValue = str(n_day)
    
    @property
    def hour(self) -> int: return int(self.__tumblerHour.currentValue)
    
    @hour.setter
    def hour(self, n_hour: int) -> None: self.__tumblerHour.currentValue = str(n_hour)
    
    @property
    def min(self) -> int: return int(self.__tumblerMin.currentValue)
    
    @min.setter
    def min(self, n_min: int) -> None: self.__tumblerMin.currentValue = str(n_min)
    
    @property
    def sec(self) -> int: return int(self.__tumblerSec.currentValue)
    
    @sec.setter
    def sec(self, n_sec: int) -> None: self.__tumblerSec.currentValue = str(n_sec)
    
    @Slot()
    def setDateTime(self, n_year: int, n_month: int, n_day: int, n_hour: int, n_min: int, n_sec: int):
        self.year = n_year
        self.month = n_month
        self.day = n_day
        self.hour = n_hour
        self.min = n_min
        self.sec = n_sec


if __name__ == '__main__':
    import sys
    from PySide2.QtCore import QDate, QTime
    from PySide2.QtWidgets import QApplication, QVBoxLayout

    class FrmTumblerDateTime(QWidget):
        def __init__(self, parent: QWidget = None):
            super(FrmTumblerDateTime, self).__init__(parent)
            self.tumblerDateTime1 = TumblerDateTime()
            self.tumblerDateTime2 = TumblerDateTime()
            self.initForm()

            layout = QVBoxLayout()
            layout.addWidget(self.tumblerDateTime1)
            layout.addWidget(self.tumblerDateTime2)
            self.setLayout(layout)

        def initForm(self):
            date: QDate = QDate.currentDate()
            time: QTime = QTime.currentTime()

            self.tumblerDateTime1.year = date.year()
            self.tumblerDateTime1.month = date.month()
            self.tumblerDateTime1.day = date.day()
            self.tumblerDateTime1.hour = time.hour()
            self.tumblerDateTime1.min = time.minute()
            self.tumblerDateTime1.sec = time.second()

            self.tumblerDateTime2.setDateTime(date.year(), date.month(), date.day(),
                                              time.hour(), time.minute(), time.second())

    app = QApplication()
    window = FrmTumblerDateTime()
    window.resize(500, 300)
    window.show()
    sys.exit(app.exec_())
