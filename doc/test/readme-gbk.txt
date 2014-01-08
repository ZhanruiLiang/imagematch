test-page.png 是配置测试参数的页面截图.
test-result-page.png 是返回测试结果的页面截图.
test.html 是配置测试参数的页面样本.
test-result.html 是返回测试结果的页面样本.
test.js 是test-result.html 页面里面的js, 用了jQuery. 里面演示了怎么获得进度和结果等数据.

对于返回测试结果的页面, 进度完成后的最终数据可以用json传进来, 格式是:

  result = [[group1, rate1], [group2, rate2], [group3, rate3], ..., ];
  averageRate = ...;

其中group1, group2, 等是组号(1, 2, ... 10). rate是正确率, 是0到1之间的数字. 
averageRate 也是是0到1的数字, 代表所有组的平均准确率.
