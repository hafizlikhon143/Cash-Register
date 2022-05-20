document.onreadystatechange = function(e){
    let prevBtn = document.querySelector(".paginate-link-prev");
    let nextBtn = document.querySelector(".paginate-link-next");
    
    prevBtn.addEventListener("click", triggerActionDown);
    nextBtn.addEventListener("click", triggerActionUp)

    function triggerActionDown(e){
        triggerAction(e, "down");
    }
    function triggerActionUp(e){
        triggerAction(e, "up");
    }
    function triggerAction(e, cmd){
        e.preventDefault();
        var pathLoc = window.location.pathname;
        var paths = pathLoc.split("/");
        
        for(i=0;i<paths.length; i++){
            if(page_num > paths[i].indexOf("page") != -1){
                var newPath = paths[i].split("=")
                if(page_num >= newPath[1] && newPath[1] >= 1){
                    if(cmd == "down" && newPath[1] != 1){
                        newPath = Number(newPath[1]) - 1;
                    }
                    else if(cmd == "up" && page_num != newPath[1]){
                        newPath = Number(newPath[1]) + 1;
                    }else{
                        newPath = 1;
                    }
                    paths = pathLoc.split('/').slice(0,2);

                    paths = paths.join("/")
                    window.location.pathname = `${paths}/page=${newPath}`;
                }
                else{
                    console.log("triggerd");
                    console.error("Wrong condition");
                }
            }
        }
    }
}