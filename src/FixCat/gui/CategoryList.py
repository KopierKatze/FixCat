"""
Copyright 2012 Alexandra Weiss, Franz Gregor

This file is part of FixCat.

FixCat is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

FixCat is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with FixCat.  If not, see <http://www.gnu.org/licenses/>.
"""
import wx

class CategoryList(wx.ListCtrl):
    def __init__(self, parent, id, seek_func=None):
        wx.ListCtrl.__init__(self, parent, id, size=(200, -1), style=wx.LC_REPORT|wx.SUNKEN_BORDER)

        self.InsertColumn(0, "Index")
        self.InsertColumn(1, "Category")
        self.SetColumnWidth(0, 60)
        self.SetColumnWidth(1, 135)

        self.order = []

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnClick)
        self.seek_func = seek_func

    def OnClick(self, event):
        if not self.seek_func is None:
            self.seek_func(self.order[event.GetIndex()][0])

    def FillInCategorisations(self, categorisation_list):
        self.DeleteAllItems()

        for index in xrange(len(self.order)):
            self.InsertStringItem(index, unicode(categorisation_list[self.order[index]][0]))
            self.SetStringItem(index, 1, unicode(categorisation_list[self.order[index]][1]))

    def SetCategorisationOrder(self, order):
        self.order = order

    def Update(self, index, name):
        self.SetStringItem(self.order.index(index), 1, name)

    def MarkFrame(self, frame):
        sel = self.GetFirstSelected()
        while sel != -1:
            self.Select(sel, False)
            sel = self.GetNextSelected(sel)

        for (start, end) in self.order:
            if frame >= start and frame <= end:
                self.Select(self.order.index((start, end)))
                self.EnsureVisible(self.order.index((start, end)))
                break

    def GetSelected(self):
        list_indices = []
        sel = self.GetFirstSelected()
        while sel != -1:
            list_indices.append(sel)
            sel = self.GetNextSelected(sel)

        category_indices = []
        for list_index in list_indices:
            category_indices.append(self.order[list_index])

        return category_indices
