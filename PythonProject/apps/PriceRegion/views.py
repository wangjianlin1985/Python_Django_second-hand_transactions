from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.PriceRegion.models import PriceRegion
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台价格区间添加
    def get(self,request):

        # 使用模板
        return render(request, 'PriceRegion/priceRegion_frontAdd.html')

    def post(self, request):
        priceRegion = PriceRegion() # 新建一个价格区间对象然后获取参数
        priceRegion.regionName = request.POST.get('priceRegion.regionName')
        priceRegion.save() # 保存价格区间信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改价格区间
    def get(self, request, regionId):
        context = {'regionId': regionId}
        return render(request, 'PriceRegion/priceRegion_frontModify.html', context)


class FrontListView(BaseView):  # 前台价格区间查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        # 然后条件组合查询过滤
        priceRegions = PriceRegion.objects.all()
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(priceRegions, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        priceRegions_page = self.paginator.page(self.currentPage)

        # 构造模板需要的参数
        context = {
            'priceRegions_page': priceRegions_page,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'PriceRegion/priceRegion_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示价格区间详情页
    def get(self, request, regionId):
        # 查询需要显示的价格区间对象
        priceRegion = PriceRegion.objects.get(regionId=regionId)
        context = {
            'priceRegion': priceRegion
        }
        # 渲染模板显示
        return render(request, 'PriceRegion/priceRegion_frontshow.html', context)


class ListAllView(View): # 前台查询所有价格区间
    def get(self,request):
        priceRegions = PriceRegion.objects.all()
        priceRegionList = []
        for priceRegion in priceRegions:
            priceRegionObj = {
                'regionId': priceRegion.regionId,
                'regionName': priceRegion.regionName,
            }
            priceRegionList.append(priceRegionObj)
        return JsonResponse(priceRegionList, safe=False)


class UpdateView(BaseView):  # Ajax方式价格区间更新
    def get(self, request, regionId):
        # GET方式请求查询价格区间对象并返回价格区间json格式
        priceRegion = PriceRegion.objects.get(regionId=regionId)
        return JsonResponse(priceRegion.getJsonObj())

    def post(self, request, regionId):
        # POST方式提交价格区间修改信息更新到数据库
        priceRegion = PriceRegion.objects.get(regionId=regionId)
        priceRegion.regionName = request.POST.get('priceRegion.regionName')
        priceRegion.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台价格区间添加
    def get(self,request):

        # 渲染显示模板界面
        return render(request, 'PriceRegion/priceRegion_add.html')

    def post(self, request):
        # POST方式处理图书添加业务
        priceRegion = PriceRegion() # 新建一个价格区间对象然后获取参数
        priceRegion.regionName = request.POST.get('priceRegion.regionName')
        priceRegion.save() # 保存价格区间信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新价格区间
    def get(self, request, regionId):
        context = {'regionId': regionId}
        return render(request, 'PriceRegion/priceRegion_modify.html', context)


class ListView(BaseView):  # 后台价格区间列表
    def get(self, request):
        # 使用模板
        return render(request, 'PriceRegion/priceRegion_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        # 然后条件组合查询过滤
        priceRegions = PriceRegion.objects.all()
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(priceRegions, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        priceRegions_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        priceRegionList = []
        for priceRegion in priceRegions_page:
            priceRegion = priceRegion.getJsonObj()
            priceRegionList.append(priceRegion)
        # 构造模板页面需要的参数
        priceRegion_res = {
            'rows': priceRegionList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(priceRegion_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除价格区间信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        regionIds = self.getStrParam(request, 'regionIds')
        regionIds = regionIds.split(',')
        count = 0
        try:
            for regionId in regionIds:
                PriceRegion.objects.get(regionId=regionId).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出价格区间信息到excel并下载
    def get(self, request):
        # 收集查询参数
        # 然后条件组合查询过滤
        priceRegions = PriceRegion.objects.all()
        #将查询结果集转换成列表
        priceRegionList = []
        for priceRegion in priceRegions:
            priceRegion = priceRegion.getJsonObj()
            priceRegionList.append(priceRegion)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(priceRegionList)
        # 设置要导入到excel的列
        columns_map = {
            'regionId': '区间id',
            'regionName': '区间名称',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'priceRegions.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="priceRegions.xlsx"'
        return response

