from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.OldLevel.models import OldLevel
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台新旧程度添加
    def get(self,request):

        # 使用模板
        return render(request, 'OldLevel/oldLevel_frontAdd.html')

    def post(self, request):
        oldLevel = OldLevel() # 新建一个新旧程度对象然后获取参数
        oldLevel.levelName = request.POST.get('oldLevel.levelName')
        oldLevel.save() # 保存新旧程度信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改新旧程度
    def get(self, request, levelId):
        context = {'levelId': levelId}
        return render(request, 'OldLevel/oldLevel_frontModify.html', context)


class FrontListView(BaseView):  # 前台新旧程度查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        # 然后条件组合查询过滤
        oldLevels = OldLevel.objects.all()
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(oldLevels, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        oldLevels_page = self.paginator.page(self.currentPage)

        # 构造模板需要的参数
        context = {
            'oldLevels_page': oldLevels_page,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'OldLevel/oldLevel_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示新旧程度详情页
    def get(self, request, levelId):
        # 查询需要显示的新旧程度对象
        oldLevel = OldLevel.objects.get(levelId=levelId)
        context = {
            'oldLevel': oldLevel
        }
        # 渲染模板显示
        return render(request, 'OldLevel/oldLevel_frontshow.html', context)


class ListAllView(View): # 前台查询所有新旧程度
    def get(self,request):
        oldLevels = OldLevel.objects.all()
        oldLevelList = []
        for oldLevel in oldLevels:
            oldLevelObj = {
                'levelId': oldLevel.levelId,
                'levelName': oldLevel.levelName,
            }
            oldLevelList.append(oldLevelObj)
        return JsonResponse(oldLevelList, safe=False)


class UpdateView(BaseView):  # Ajax方式新旧程度更新
    def get(self, request, levelId):
        # GET方式请求查询新旧程度对象并返回新旧程度json格式
        oldLevel = OldLevel.objects.get(levelId=levelId)
        return JsonResponse(oldLevel.getJsonObj())

    def post(self, request, levelId):
        # POST方式提交新旧程度修改信息更新到数据库
        oldLevel = OldLevel.objects.get(levelId=levelId)
        oldLevel.levelName = request.POST.get('oldLevel.levelName')
        oldLevel.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台新旧程度添加
    def get(self,request):

        # 渲染显示模板界面
        return render(request, 'OldLevel/oldLevel_add.html')

    def post(self, request):
        # POST方式处理图书添加业务
        oldLevel = OldLevel() # 新建一个新旧程度对象然后获取参数
        oldLevel.levelName = request.POST.get('oldLevel.levelName')
        oldLevel.save() # 保存新旧程度信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新新旧程度
    def get(self, request, levelId):
        context = {'levelId': levelId}
        return render(request, 'OldLevel/oldLevel_modify.html', context)


class ListView(BaseView):  # 后台新旧程度列表
    def get(self, request):
        # 使用模板
        return render(request, 'OldLevel/oldLevel_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        # 然后条件组合查询过滤
        oldLevels = OldLevel.objects.all()
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(oldLevels, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        oldLevels_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        oldLevelList = []
        for oldLevel in oldLevels_page:
            oldLevel = oldLevel.getJsonObj()
            oldLevelList.append(oldLevel)
        # 构造模板页面需要的参数
        oldLevel_res = {
            'rows': oldLevelList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(oldLevel_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除新旧程度信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        levelIds = self.getStrParam(request, 'levelIds')
        levelIds = levelIds.split(',')
        count = 0
        try:
            for levelId in levelIds:
                OldLevel.objects.get(levelId=levelId).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出新旧程度信息到excel并下载
    def get(self, request):
        # 收集查询参数
        # 然后条件组合查询过滤
        oldLevels = OldLevel.objects.all()
        #将查询结果集转换成列表
        oldLevelList = []
        for oldLevel in oldLevels:
            oldLevel = oldLevel.getJsonObj()
            oldLevelList.append(oldLevel)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(oldLevelList)
        # 设置要导入到excel的列
        columns_map = {
            'levelId': '新旧程度id',
            'levelName': '新旧程度名称',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'oldLevels.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="oldLevels.xlsx"'
        return response

