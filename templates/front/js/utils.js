/**
 * 页面跳转
 * @param {Object} url
 */
function jump(url) {
	if (!url || url == 'null' || url == null) {
		window.location.href = './index.html';
	}
	
	// 添加页面过渡效果
	document.body.style.transition = 'opacity 0.3s ease';
	document.body.style.opacity = '0';
	
	// 路径访问设置
	localStorage.setItem('iframeUrl', url.replace('../', './pages/'));
	
	// 延迟跳转，等待过渡效果完成
	setTimeout(function() {
		window.location.href = url;
	}, 300);
}

/**
 * 返回
 */
function back(num = -1) {
	window.history.go(num)
}

/**
 * 生成订单
 */
function genTradeNo() {
	var date = new Date();
	var tradeNo = date.getFullYear().toString() + (date.getMonth() + 1).toString() +
		date.getDate().toString() + date.getHours().toString() + date.getMinutes().toString() +
		date.getSeconds().toString() + date.getMilliseconds().toString();
	for (var i = 0; i < 5; i++) //5位随机数，用以加在时间戳后面。
	{
		tradeNo += Math.floor(Math.random() * 10);
	}
	return tradeNo;
}
