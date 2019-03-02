from app.models import Post


# 添加收藏
def add_favorite(self, pid):
    p = Post.query.get(pid)
    self.favorites.append(p)


# 取消收藏
def del_favorite(self, pid):
    p = Post.query.get(pid)
    self.favorites.remove(p)


# 判断是否已经收藏
def is_favorite(self, pid):
    # 获取所有收藏的博客
    favorites = self.favorites.all()
    posts = list(filter(lambda p: p.id == pid, favorites))
    if len(posts) > 0:
        return True
    return False
