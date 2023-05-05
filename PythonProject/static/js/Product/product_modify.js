$(function () {
    //实例化商品描述编辑器
    tinyMCE.init({
        selector: "#product_productDesc_modify",
        theme: 'advanced',
        language: "zh",
        strict_loading_mode: 1,
    });
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/Product/update/" + $("#product_productId_modify").val(),
		type : "get",
		data : {
			//productId : $("#product_productId_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (product, response, status) {
			$.messager.progress("close");
			if (product) { 
				$("#product_productId_modify").val(product.productId);
				$("#product_productId_modify").validatebox({
					required : true,
					missingMessage : "请输入商品id",
					editable: false
				});
				$("#product_productClassObj_classId_modify").combobox({
					url:"/ProductClass/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"classId",
					textField:"className",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#product_productClassObj_classId_modify").combobox("select", product.productClassObjPri);
						//var data = $("#product_productClassObj_classId_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#product_productClassObj_classId_edit").combobox("select", data[0].classId);
						//}
					}
				});
				$("#product_productName_modify").val(product.productName);
				$("#product_productName_modify").validatebox({
					required : true,
					missingMessage : "请输入商品名称",
				});
				$("#product_mainPhotoImgMod").attr("src", product.mainPhoto);
				$("#product_oldLevel_levelId_modify").combobox({
					url:"/OldLevel/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"levelId",
					textField:"levelName",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#product_oldLevel_levelId_modify").combobox("select", product.oldLevelPri);
						//var data = $("#product_oldLevel_levelId_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#product_oldLevel_levelId_edit").combobox("select", data[0].levelId);
						//}
					}
				});
				$("#product_priceRegionObj_regionId_modify").combobox({
					url:"/PriceRegion/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"regionId",
					textField:"regionName",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#product_priceRegionObj_regionId_modify").combobox("select", product.priceRegionObjPri);
						//var data = $("#product_priceRegionObj_regionId_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#product_priceRegionObj_regionId_edit").combobox("select", data[0].regionId);
						//}
					}
				});
				$("#product_price_modify").val(product.price);
				$("#product_price_modify").validatebox({
					required : true,
					validType : "number",
					missingMessage : "请输入商品价格",
					invalidMessage : "商品价格输入不对",
				});
				$("#product_areaObj_areaId_modify").combobox({
					url:"/AreaInfo/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"areaId",
					textField:"areaName",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#product_areaObj_areaId_modify").combobox("select", product.areaObjPri);
						//var data = $("#product_areaObj_areaId_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#product_areaObj_areaId_edit").combobox("select", data[0].areaId);
						//}
					}
				});
				tinyMCE.editors['product_productDesc_modify'].setContent(product.productDesc);
				$("#product_connectPerson_modify").val(product.connectPerson);
				$("#product_connectPerson_modify").validatebox({
					required : true,
					missingMessage : "请输入联系人",
				});
				$("#product_connectPhone_modify").val(product.connectPhone);
				$("#product_connectPhone_modify").validatebox({
					required : true,
					missingMessage : "请输入联系电话",
				});
				$("#product_userObj_user_name_modify").combobox({
					url:"/UserInfo/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"user_name",
					textField:"name",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#product_userObj_user_name_modify").combobox("select", product.userObjPri);
						//var data = $("#product_userObj_user_name_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#product_userObj_user_name_edit").combobox("select", data[0].user_name);
						//}
					}
				});
				$("#product_addTime_modify").datetimebox({
					value: product.addTime,
					required: true,
					showSeconds: true,
				});
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#productModifyButton").click(function(){ 
		if ($("#productModifyForm").form("validate")) {
			$("#productModifyForm").form({
			    url:"Product/update/" + $("#product_productId_modify").val(),
			    onSubmit: function(){
					if($("#productEditForm").form("validate"))  {
	                	$.messager.progress({
							text : "正在提交数据中...",
						});
	                	return true;
	                } else {
	                    return false;
	                }
			    },
			    success:function(data){
			    	$.messager.progress("close");
                	var obj = jQuery.parseJSON(data);
                    if(obj.success){
                        $.messager.alert("消息","信息修改成功！");
                        $(".messager-window").css("z-index",10000);
                        //location.href="frontlist";
                    }else{
                        $.messager.alert("消息",obj.message);
                        $(".messager-window").css("z-index",10000);
                    } 
			    }
			});
			//提交表单
			$("#productModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});
