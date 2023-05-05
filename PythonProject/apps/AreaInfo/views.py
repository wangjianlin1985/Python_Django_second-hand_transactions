from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.AreaInfo.models import AreaInfo
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台所在区域添加
    def get(self,request):

        # 使用模板
        return render(request, 'AreaInfo/areaInfo_frontAdd.html')

    def post(self, request):
        areaInfo = AreaInfo() # 新建一个所在区域对象然后获取参数
        areaInfo.areaName = request.POST.get('areaInfo.areaName')
        areaInfo.save() # 保存所在区域信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改所在区域
    def get(self, request, areaId):
        context = {'areaId': areaId}
        return render(request, 'AreaInfo/areaInfo_frontModify.html', context)


class FrontListView(BaseView):  # 前台所在区域查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        # 然后条件组合查询过滤
        areaInfos = AreaInfo.objects.all()
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(areaInfos, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        areaInfos_page = self.paginator.page(self.currentPage)

        # 构造模板需要的参数
        context = {
            'areaInfos_page': areaInfos_page,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'AreaInfo/areaInfo_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示所在区域详情页
    def get(self, request, areaId):
        # 查询需要显示的所在区域对象
        areaInfo = AreaInfo.objects.get(areaId=areaId)
        context = {
            'areaInfo': areaInfo
        }
        # 渲染模板显示
        return render(request, 'AreaInfo/areaInfo_frontshow.html', context)


class ListAllView(View): # 前台查询所有所在区域
    def get(self,request):
        areaInfos = AreaInfo.objects.all()
        areaInfoList = []
        for areaInfo in areaInfos:
            areaInfoObj = {
                'areaId': areaInfo.areaId,
                'areaName': areaInfo.areaName,
            }
            areaInfoList.append(areaInfoObj)
        return JsonResponse(areaInfoList, safe=False)


class UpdateView(BaseView):  # Ajax方式所在区域更新
    def get(self, request, areaId):
        # GET方式请求查询所在区域对象并返回所在区域json格式
        areaInfo = AreaInfo.objects.get(areaId=areaId)
        return JsonResponse(areaInfo.getJsonObj())

    def post(self, request, areaId):
        # POST方式提交所在区域修改信息更新到数据库
        areaInfo = AreaInfo.objects.get(areaId=areaId)
        areaInfo.areaName = request.POST.get('areaInfo.areaName')
        areaInfo.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台所在区域添加
    def get(self,request):

        # 渲染显示模板界面
        return render(request, 'AreaInfo/areaInfo_add.html')

    def post(self, request):
        # POST方式处理图书添加业务
        areaInfo = AreaInfo() # 新建一个所在区域对象然后获取参数
        areaInfo.areaName = request.POST.get('areaInfo.areaName')
        areaInfo.save() # 保存所在区域信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新所在区域
    def get(self, request, areaId):
        context = {'areaId': areaId}
        return render(request, 'AreaInfo/areaInfo_modify.html', context)


class ListView(BaseView):  # 后台所在区域列表
    def get(self, request):
        # 使用模板
        return render(request, 'AreaInfo/areaInfo_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        # 然后条件组合查询过滤
        areaInfos = AreaInfo.objects.all()
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(areaInfos, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        areaInfos_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        areaInfoList = []
        for areaInfo in areaInfos_page:
            areaInfo = areaInfo.getJsonObj()
            areaInfoList.append(areaInfo)
        # 构造模板页面需要的参数
        areaInfo_res = {
            'rows': areaInfoList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(areaInfo_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除所在区域信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        areaIds = self.getStrParam(request, 'areaIds')
        areaIds = areaIds.split(',')
        count = 0
        try:
            for areaId in areaIds:
                AreaInfo.objects.get(areaId=areaId).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出所在区域信息到excel并下载
    def get(self, request):
        # 收集查询参数
        # 然后条件组合查询过滤
        areaInfos = AreaInfo.objects.all()
        #将查询结果集转换成列表
        areaInfoList = []
        for areaInfo in areaInfos:
            areaInfo = areaInfo.getJsonObj()
            areaInfoList.append(areaInfo)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(areaInfoList)
        # 设置要导入到excel的列
        columns_map = {
            'areaId': '区域id',
            'areaName': '区域名称',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'areaInfos.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="areaInfos.xlsx"'
        return response

