const base = {
    get() {
                return {
            url : "http://localhost:8080/dj_intellrnmgmtsystem/",
            name: "dj_intellrnmgmtsystem",
            // 退出到首页链接
            indexUrl: 'http://localhost:8080/dj_intellrnmgmtsystem/front/index.html'
        };
            },
    getProjectName(){
        return {
            projectName: "智能化学习管理系统"
        } 
    }
}
export default base
