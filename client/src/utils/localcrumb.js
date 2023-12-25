export const getCrumb = () => {
    const defaultCrumb = [
        {
            path: "/",
            name: "home",
            label: "首页",
            icon: "s-home",
            url: "Home/Home",
        }
    ]
    const result = localStorage.getItem('crumbList')
    return result ? JSON.parse(result) : defaultCrumb
}

export const saveCrumb = (obj) => {
    localStorage.setItem('crumbList', JSON.stringify(obj))
}