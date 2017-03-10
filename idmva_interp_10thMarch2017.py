import ROOT
import math, array, sys
from optparse import OptionParser
import hggStyle

ROOT.gROOT.SetBatch()
style = hggStyle.hggStyle()
ROOT.gROOT.SetStyle("hggPaperStyle")
ROOT.gROOT.ForceStyle()

ROOT.myColorA1 = ROOT.TColor.GetColor("#303083")
ROOT.myColorA2 = ROOT.TColor.GetColor("#8a8ab9")
ROOT.myColorA3 = ROOT.TColor.GetColor("#9e9ec5")
ROOT.myColorA3tr = ROOT.TColor.GetColor("#9e9ec4")
ROOT.gROOT.GetColor(ROOT.myColorA3tr).SetAlpha(0.5)
ROOT.myColorA4 = ROOT.TColor.GetColor("#cecee2")

ROOT.myColorB0 = ROOT.TColor.GetColor("#540000")
ROOT.myColorB1 = ROOT.TColor.GetColor("#cc0000")
ROOT.myColorB2 = ROOT.TColor.GetColor("#e65353")
ROOT.myColorB3 = ROOT.TColor.GetColor("#f7baba")
ROOT.myColorB3tr = ROOT.TColor.GetColor("#f7babb")
ROOT.gROOT.GetColor(ROOT.myColorB3tr).SetAlpha(0.5)
ROOT.myColorB4 = ROOT.TColor.GetColor("#f29191")    

ROOT.myColorB5 = ROOT.TColor.GetColor("#FBDDDD")
ci = 1756
myNewColor = ROOT.TColor(ci, 1.0, 0., 0., "", 0.5)
ci2 = 1974
myNewColor2 = ROOT.TColor(ci2, .75, .75, .75, "", 0.5)

parser = OptionParser()
parser.add_option("-d", "--data", default="histograms_CMS-HGG_zeevalidation.root", help="Input file for data. \Default: %default")
parser.add_option("-m", "--mc", default="histograms_CMS-HGG_zeevalidation_david_template_envelopes.root", help="Input file for MC. \Default: %default")
parser.add_option("-p", "--passMva", default=False, action="store_true", help="Select events passing diphoton MVA min cut.")
parser.add_option("-n", "--normalize", default=True, action="store_true", help="Normalize to same area")
parser.add_option("-r", "--rarity", default=False, action="store_true", help="Trasformed plot with signal rarity")
parser.add_option("-t", "--TeV", default=8, help="Setup for 7TeV data")
(options, arg) = parser.parse_args()

ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

#ROOT.gStyle.SetCanvasColor(0)
#ROOT.gStyle.SetFrameBorderMode(0)
#ROOT.gStyle.SetPalette(1)
#ROOT.gStyle.SetLineColor(1)

txt1 = []
legends = []
ratio = []
ratio_syst = []
ratio_syst_up = []
ratio_syst_down = []
hist_syst = []
hist_syst_up = []
hist_syst_down = []
mc_temp = []
graphs = []
ratio_graphs= []

def plotRatio(cat, data, mc, mc_top, mc_bottom, passMVAcut, equalArea):
    global ratio, ratio_syst, ratio_syst_up, ratio_syst_down
    global ratio_graphs

    ratio_syst.append(mc[cat].Clone())
    #ratio_syst.append(mc_bottom[cat].Clone())
    #ratio_syst[-1].Add(mc_top[cat].Clone())
    #ratio_syst[-1].Scale(0.5)
    x = array.array('f', [])
    y = array.array('f', [])
    eyu = array.array('f', [])
    eyd = array.array('f', [])
    exu = array.array('f', [])
    exd = array.array('f', [])

    ratio_syst_up.append(ratio_syst[-1].Clone())
    ratio_syst_down.append(ratio_syst[-1].Clone())
           
    sf = 1
    if (passMVAcut):
        sf = data[cat].Integral(48,100)/mc[cat].Integral(48,100)
    else:
        sf = data[cat].Integral()/mc[cat].Integral()
    if (not equalArea):
        sf = data[0].Integral()/mc[0].Integral()
    
    mc[cat].Scale(sf)
    ratio_syst[-1].Scale(sf)
    ratio_syst_up[-1].Scale(sf)
    ratio_syst_down[-1].Scale(sf)

    for i in xrange(1, ratio_syst[-1].GetNbinsX()+1):
        up   = math.sqrt(math.pow(mc_top[cat].GetBinContent(i)-mc[cat].GetBinContent(i),2))
        down = math.sqrt(math.pow(mc_bottom[cat].GetBinContent(i)-mc[cat].GetBinContent(i),2))
        
        up2 = mc_top[cat].GetBinContent(i)-mc[cat].GetBinContent(i)
        down2 = -mc_bottom[cat].GetBinContent(i)+mc[cat].GetBinContent(i)

        x.append(ratio_syst[-1].GetXaxis().GetBinCenter(i))
        y.append(ratio_syst[-1].GetBinContent(i))
        #eyu.append(up)
        #eyd.append(down)
        eyu.append(up2)
        eyd.append(down2)

        exu.append(ratio_syst[-1].GetXaxis().GetBinWidth(i)/2.0) # changed from 1 to "i"
        exd.append(ratio_syst[-1].GetXaxis().GetBinWidth(i)/2.0) # changed from 1 to "i"
        ratio_syst_up[-1].SetBinContent(i, ratio_syst[-1].GetBinContent(i)+up2);
        ratio_syst_down[-1].SetBinContent(i, ratio_syst[-1].GetBinContent(i)-down2);
 
    for i in xrange(hist_syst[-1].GetNbinsX()):
        if (mc[cat].GetBinContent(i+1) !=0):
            y[i] = y[i]/mc[cat].GetBinContent(i+1)
            eyd[i] = eyd[i]/mc[cat].GetBinContent(i+1)
            eyu[i] = eyu[i]/mc[cat].GetBinContent(i+1)
        else:
            y[i] = 0
    #x.insert(0, -1.01)
    #exu.insert(0, exu[0])
    #exd.insert(0, exd[0])
    #eyu.insert(0, eyu[0])
    #eyd.insert(0, eyu[0])
    #y.insert(0, y[0])
    #
    #x.append(1.01)
    #exu.append(exu[-1])
    #exd.append(exd[-1])
    #eyu.append(eyu[-1])
    #eyd.append(eyu[-1])
    #y.append(y[-1])

    ratio.append(data[cat].Clone("ratio"+str(cat)))
    ratio[-1].Divide(mc[cat])
    ratio_syst[-1].Divide(mc[cat])
    ratio_syst_up[-1].Divide(mc[cat])
    ratio_syst_down[-1].Divide(mc[cat])

    #for i in xrange(ratio_syst[-1].GetNbinsX()):
    #    print ratio_syst[-1].GetBinContent(i), ratio_syst_up[-1].GetBinContent(i),ratio_syst_down[-1].GetBinContent(i)
    
    ratio[-1].Draw("e")
    ratio[-1].GetYaxis().SetRangeUser(0.1, 1.9)
    ratio_graphs.append(ROOT.TGraphAsymmErrors(len(x), x, y, exd, exu, eyd, eyu))
    ratio_graphs[-1].SetFillColor(ROOT.myColorB5) #gouranga
    ratio_graphs[-1].SetFillStyle(3001)
    ratio_graphs[-1].SetLineColor(ROOT.myColorB3tr)
    ratio_graphs[-1].Draw("e2,same")
    ratio_syst_up[-1].SetLineColor(ROOT.myColorB2)
    ratio_syst_down[-1].SetLineColor(2)
    ratio_syst_up[-1].Draw("hist,same")
    ratio_syst_down[-1].Draw("hist,same")
    ratio[-1].SetMarkerSize(0.5)
    ratio[-1].SetLineColor(ROOT.kBlack)
    ratio[-1].Draw("e,same")
     #ROOT.gPad.SetGridx()
    ROOT.gPad.SetGridy()
    ROOT.gPad.RedrawAxis()
    return ratio[-1]
    

def plotDataMC(cat, data, mc, mc_top, mc_bottom, passMVAcut, equalArea, xaxis, norm, legend):
    #......... (0, data, mc, mc_top, mc_bottom, False,       True        xasix, True, false)
    global hist_syst, hist_syst_up, hist_syst_down, mc_temp
    global graphs

    mc_temp.append(mc[cat].Clone())
    hist_syst.append(mc[cat].Clone())
    mc_temp[-1].SetFillColor(ROOT.myColorA3)
    mc_temp[-1].SetLineColor(ROOT.myColorA2)
    #hist_syst.append(mc_bottom[cat].Clone())
    #hist_syst[-1].Add(mc_top[cat].Clone())
    #hist_syst[-1].Scale(0.5)
    x = array.array('f', [])
    y = array.array('f', [])
    eyu = array.array('f', [])
    eyd = array.array('f', [])
    exu = array.array('f', [])
    exd = array.array('f', [])

    hist_syst_up.append(hist_syst[-1].Clone())
    hist_syst_down.append(hist_syst[-1].Clone())

    sf = 1
    if (norm):
        if (passMVAcut):
            sf = data[cat].Integral(48,100)/mc_temp[-1].Integral(48,100)
        else:
            sf = data[cat].Integral()/mc_temp[-1].Integral()
        if (not equalArea):
            sf = data[0].Integral()/mc[0].Integral()
    print "sf", sf   
    #sf = 1
    #print "sf after", sf
    #print "before sf"
    #print "mc_temp[-1].GetMaximum()", mc_temp[-1].GetMaximum()
    #print "mc_top[cat]", mc_top[cat].GetMaximum()
    #print "mc_bottom[cat]", mc_bottom[cat].GetMaximum()

    mc_temp[-1].Scale(sf)
    hist_syst[-1].Scale(sf)
    mc_top[cat].Scale(sf)
    mc_bottom[cat].Scale(sf)

    #print "after sf"
    print "mc_temp[-1].GetMaximum()", mc_temp[-1].GetMaximum()
    print "mc_temp[-1].Integral()", mc_temp[-1].Integral()
    print "mc_top[cat].GetMaximum()", mc_top[cat].GetMaximum()
    print "mc_top[cat].Integral()", mc_top[cat].Integral()
    print "mc_bottom[cat].GetMaximum()", mc_bottom[cat].GetMaximum()

    sumbin = 0.0
    sumup = 0.0

    for i in xrange(1, hist_syst[-1].GetNbinsX()+1):
        up   = math.sqrt(math.pow(mc_top[cat].GetBinContent(i)-hist_syst[-1].GetBinContent(i),2))
        down = math.sqrt(math.pow(mc_bottom[cat].GetBinContent(i)-hist_syst[-1].GetBinContent(i),2))

        #print "up", up
        up2 = mc_top[cat].GetBinContent(i)-hist_syst[-1].GetBinContent(i)
        #print "up2", up2


        down2 = -mc_bottom[cat].GetBinContent(i)+hist_syst[-1].GetBinContent(i)

        x.append(hist_syst[-1].GetXaxis().GetBinCenter(i))
        y.append(hist_syst[-1].GetBinContent(i))
        eyu.append(up2)
        eyd.append(down2)
        exu.append(hist_syst[-1].GetXaxis().GetBinWidth(i)/2.0) # change from [1] to i
        exd.append(hist_syst[-1].GetXaxis().GetBinWidth(i)/2.0) # change from [1] to i
        #hist_syst_up[-1].SetBinContent(i, mc_top[-1].GetBinContent(i)) # test
        #hist_syst_down[-1].SetBinContent(i, mc_bottom[-1].GetBinContent(i)) #test
        #sumup = sumup + up
        #sumbin = hist_syst[-1].GetBinContent(i)+up2
        hist_syst_up[-1].SetBinContent(i, hist_syst[-1].GetBinContent(i)+up2); # 10th March
        hist_syst_down[-1].SetBinContent(i, hist_syst[-1].GetBinContent(i)-down2); # 10th March
    
    #print "sumbin", sumbin
    #print "sumup", sumup
    #print "debug after for loop"
    #print "x=", x
    #print "sum(x)",sum(x)

    #for i in xrange(1, hist_syst[-1].GetNbinsX()+1):
    #    print "aa",hist_syst[-1].GetBinContent(i)
        #print "duplicate aa", len(x), hist_syst[-1].GetNbinsX()+1
    
    print "after for loop "
    print "hist_syst[-1].GetMaximum()", hist_syst[-1].GetMaximum()
    print "hist_syst[-1].Integral()",hist_syst[-1].Integral()
    print "hist_syst_up[-1].GetMaximum()", hist_syst_up[-1].GetMaximum()
    print "hist_syst_up[-1].Integral()", hist_syst_up[-1].Integral()
    print "hist_syst_down[-1].GetMaximum()", hist_syst_down[-1].GetMaximum()
    #x.insert(0, -1.01)
    #exu.insert(0, exu[0])
    #exd.insert(0, exd[0])
    #eyu.insert(0, eyu[0])
    #eyd.insert(0, eyu[0])
    #y.insert(0, y[0])
    #
    #x.append(1.01)
    #exu.append(exu[-1])
    #exd.append(exd[-1])
    #eyu.append(eyu[-1])
    #eyd.append(eyu[-1])
    #y.append(y[-1])

    graphs.append(ROOT.TGraphAsymmErrors(len(x), x, y, exd, exu, eyd, eyu))
    graphs[-1].SetFillColor(ROOT.myColorB3tr)
    if (options.TeV == 8):
        legends.append(ROOT.TLegend(.20,.65,.40,.85)) #.60,.60,.85,.85
    else:
        legends.append(ROOT.TLegend(.15,.65,.40,.85))
    legends[-1].SetBorderSize(0);
    #legends[-1].SetFillColor(10);
    legends[-1].SetTextSize(.045);
    legends[-1].AddEntry(data[0],"Data", "PE");
    legends[-1].AddEntry(mc_temp[-1],"Z#rightarrowee MC","F");
    legends[-1].AddEntry(graphs[-1],"MC syst.","F");
    data[cat].Draw("pe")
    if (legend):
        legends[-1].Draw("same")
    #txt1[-1].Draw("SAME")
    #data[cat].SetMaximum(data[cat].GetMaximum()*1.3)
    data[cat].GetXaxis().SetTitle(xaxis[cat])
    #data[cat].GetYaxis().SetTitleSize(0.05)
    #data[cat].GetYaxis().SetTitleOffset(1.1)
    #data[cat].GetYaxis().SetLabelSize(0.045)
    #data[cat].GetYaxis().SetTitleFont(62)
    #data[cat].GetYaxis().SetLabelFont(62)
    
    data[cat].GetYaxis().SetTitle("Events/0.02")
    mc_temp[-1].Draw("hist,same")
    graphs[-1].SetFillColor(ROOT.myColorB5) #gouranga
    graphs[-1].SetFillStyle(3001)
    graphs[-1].Draw("e2,same") #10/03
    hist_syst_up[-1].SetLineColor(ROOT.kRed) #10/03 from Red 
    #hist_syst_up[-1].SetFillColor(5) # gouranga
    hist_syst_down[-1].SetLineColor(2)

    mc_top[-1].SetLineColor(ROOT.kGreen) #10/03
    mc_bottom[-1].SetLineColor(2) #10/03
    #mc_top[-1].Draw("hist,same") #10/03
    #mc_bottom[-1].Draw("hist,same") #10/03
    hist_syst_up[-1].Draw("hist,same")
    hist_syst_down[-1].Draw("hist,same")
    data[cat].Draw("pe,same")
    ROOT.gPad.RedrawAxis()


fMC = ROOT.TFile(options.mc)
fData   = ROOT.TFile(options.data)
data = []
mc = []
mc_top = []
mc_bottom = []

#prefixes  = ["pho1_phoidMva_EB_nvtxlt15_cat0", "pho1_phoidMva_EE_nvtxlt15_cat0"#,
#             "pho2_phoidMva_EB_nvtxlt15_cat0", "pho2_phoidMva_EE_nvtxlt15_cat0"]


prefixes_data = ["idmva1_cat0_SingleElectron", "idmva2_cat0_SingleElectron"]
prefixes_mc   = ["idmva1_cat0_DYToEE", "idmva2_cat0_DYToEE"]


fData.cd()
for i, prefix in enumerate(prefixes_data):
    if (i == 0):
        data.append(fData.Get(prefix))
        data[-1].SetMarkerStyle(20)
        data[-1].GetXaxis().SetRangeUser(-0.9, 1.)
        data[-1].Sumw2(1)
    else:
        data[-1].Add(fData.Get(prefix))
data[-1].Scale(1./1000.)

fMC.cd()
for i, prefix in enumerate(prefixes_mc):
    if (i == 0):
        mc.append(fMC.Get(prefix))
        mc[-1].Sumw2()
        mc[-1].GetXaxis().SetRangeUser(-0.9, 1.)
        mc_top.append(fMC.Get(prefix+"_top"))
        mc_top[-1].Sumw2()
        mc_bottom.append(fMC.Get(prefix+"_bottom"))
        mc_bottom[-1].Sumw2()
    else:
        mc[-1].Add(fMC.Get(prefix))
        mc_top[-1].Add(fMC.Get(prefix+"_top"))
        mc_bottom[-1].Add(fMC.Get(prefix+"_bottom"))

xaxis = ["Photon ID BDT score"]
c_single = ROOT.TCanvas("c_single","BDT output",1600,800)
r = 0.26
epsilon = 0.14;
pad1 = ROOT.TPad("pad1", "pad1", 0.05, r-epsilon, .495, 1.)
#pad1.SetBorderSize(1)
#pad1.SetBorderMode(1)
pad1.SetBottomMargin(epsilon)
c_single.cd()
pad1.Draw()
pad1.cd()
#plotDataMC(0, data, mc, mc_top, mc_bottom, False, True, xaxis, True, True)
plotDataMC(0, data, mc, mc_top, mc_bottom, False, True, xaxis, True, True)
pad1.GetPrimitive(data[-1].GetName()).SetLabelSize(0)
pad1.GetPrimitive(data[-1].GetName()).GetYaxis().SetRangeUser(0, 1180.) #gouranga
pad1.GetPrimitive(data[-1].GetName()).GetYaxis().SetLabelSize(0.035)
pad1.GetPrimitive(data[-1].GetName()).GetYaxis().SetTitleOffset(1.2)
pad1.GetPrimitive(data[-1].GetName()).GetXaxis().SetTitleSize(0)
pad1.RedrawAxis()
txt1.append(ROOT.TLatex())
txt1[-1].SetNDC()
txt2 = txt1[-1]
txt1[-1].SetTextSize(0.05)
#txt1[-1].SetTextAlign(12)
if (options.TeV == 8):
    txt2.DrawLatex(0.09, 0.91, "#scale[0.5]{#times10^{3}}")
    txt1[-1].DrawLatex(0.13, 0.93, "#bf{CMS} #it{Preliminary}")
    txt1[-1].DrawLatex(0.55, 0.93, "35.9 fb^{-1} (13 TeV)")
else:
    txt1[-1].DrawLatex(0.15, 0.93, "#scale[0.8]{CMS #sqrt{s}=7 TeV; L=5.1 fb^{-1}}")
txt1[-1].Draw()
txt1.append(ROOT.TLatex())
txt1[-1].SetNDC()
txt1[-1].SetTextSize(0.05)
#txt1[-1].SetTextAlign(12)
txt1[-1].DrawLatex(0.21, 0.55, "|#eta_{#gamma}| < 1.444")
txt1[-1].Draw()

c_single.cd()
pad2 = ROOT.TPad("pad2", "pad2", 0.05, 0.0, 0.495, r*(1-epsilon))
pad2.SetTopMargin(0.)
pad2.SetBottomMargin(0.4)
pad2.SetFrameFillStyle(4000)
pad2.Draw()
pad2.cd()
plotRatio(0, data, mc, mc_top, mc_bottom, False, True)
pad2.GetPrimitive("ratio0").GetXaxis().SetLabelSize(0.16)
pad2.GetPrimitive("ratio0").GetYaxis().SetLabelSize(0.12)
pad2.GetPrimitive("ratio0").GetXaxis().SetTitleSize(0.20)
pad2.GetPrimitive("ratio0").GetYaxis().SetTitleSize(0.16)
pad2.GetPrimitive("ratio0").GetYaxis().SetTitleOffset(0.3)
pad2.GetPrimitive("ratio0").GetYaxis().SetNdivisions(105)
pad2.GetPrimitive("ratio0").GetYaxis().SetTitle("Data/MC")
lines = []
lines.append(ROOT.TLine(-.9, 1, 1., 1))
lines[-1].SetLineWidth(2)
lines[-1].SetLineColor(ROOT.kBlack)
lines[-1].Draw("SAME")

data = []
mc = []
mc_top = []
mc_bottom = []

#prefixes  = ["pho1_phoidMva_EB_nvtxgt15_cat0", "pho1_phoidMva_EB_nvtxgt15_cat0",
#             "pho2_phoidMva_EE_nvtxgt15_cat0","pho2_phoidMva_EE_nvtxgt15_cat0"]

prefixes_data = ["idmva1_cat1_SingleElectron", "idmva2_cat1_SingleElectron"]
prefixes_mc   = ["idmva1_cat1_DYToEE", "idmva2_cat1_DYToEE"]
#prefixes  = ["idmva_nom_EE"]

fData.cd()
for i, prefix in enumerate(prefixes_data):
    if (i == 0):
        data.append(fData.Get(prefix))
        data[-1].SetMarkerStyle(20)
        data[-1].Sumw2(1)
        data[-1].GetXaxis().SetRangeUser(-0.9, 1.)
    else:
        data[-1].Add(fData.Get(prefix))
data[-1].Scale(1./1000.)

fMC.cd()
for i, prefix in enumerate(prefixes_mc):
    if (i == 0):
        mc.append(fMC.Get(prefix))
        mc[-1].Sumw2()
        mc_top.append(fMC.Get(prefix+"_top"))
        mc[-1].Sumw2()
        mc_bottom.append(fMC.Get(prefix+"_bottom"))
        mc[-1].Sumw2()
    else:
        mc[-1].Add(fMC.Get(prefix))
        mc_top[-1].Add(fMC.Get(prefix+"_top"))
        mc_bottom[-1].Add(fMC.Get(prefix+"_bottom"))

r = 0.26
epsilon = 0.14;
pad3 = ROOT.TPad("pad3", "pad3", .505, r-epsilon, .955, 1.)
#pad3.SetBorderSize(1)
#pad3.SetBorderMode(1)
pad3.SetBottomMargin(epsilon)
c_single.cd()
pad3.Draw()
pad3.cd()
plotDataMC(0, data, mc, mc_top, mc_bottom, False, True, xaxis, True, True)
pad3.GetPrimitive(data[-1].GetName()).SetLabelSize(0)
pad3.GetPrimitive(data[-1].GetName()).GetYaxis().SetRangeUser(0, 180.0)#gouranga
pad3.GetPrimitive(data[-1].GetName()).GetYaxis().SetTitleOffset(1.2)
pad3.RedrawAxis()
txt1.append(ROOT.TLatex())
txt1[-1].SetNDC()
txt2 = txt1[-1]
txt1[-1].SetTextSize(0.05)
#txt1[-1].SetTextAlign(12)
if (options.TeV == 8):
    txt2.DrawLatex(0.09, 0.91, "#scale[0.5]{#times10^{3}}")
    txt1[-1].DrawLatex(0.13, 0.93, "#bf{CMS} #it{Preliminary}")
    txt1[-1].DrawLatex(0.55, 0.93, "35.9 fb^{-1} (13 TeV)")
else:
    txt1[-1].DrawLatex(0.15, 0.93, "#scale[0.8]{6.2 fb^{-1} (13TeV)}")
txt1[-1].Draw()
txt1.append(ROOT.TLatex())
txt1[-1].SetNDC()
txt1[-1].SetTextSize(0.05)
#txt1[-1].SetTextAlign(12)
txt1[-1].DrawLatex(0.21, 0.55, "|#eta_{#gamma}| > 1.566")
txt1[-1].Draw()

c_single.cd()
pad4 = ROOT.TPad("pad4", "pad4", .505, 0.0, 0.955, r*(1-epsilon))
pad4.SetTopMargin(0.)
pad4.SetBottomMargin(0.4)
#pad4.SetFrameFillStyle(4000)
pad4.Draw()
pad4.cd()
plotRatio(0, data, mc, mc_top, mc_bottom, False, True)
pad4.GetPrimitive("ratio0").GetXaxis().SetLabelSize(0.16)
pad4.GetPrimitive("ratio0").GetYaxis().SetLabelSize(0.12)
pad4.GetPrimitive("ratio0").GetXaxis().SetTitleSize(0.20)
pad4.GetPrimitive("ratio0").GetYaxis().SetTitleSize(0.16)
pad4.GetPrimitive("ratio0").GetYaxis().SetTitleOffset(0.3)
pad4.GetPrimitive("ratio0").GetYaxis().SetNdivisions(105)
pad4.GetPrimitive("ratio0").GetYaxis().SetTitle("Data/MC")
lines.append(ROOT.TLine(-.9, 1, 1, 1))
lines[-1].SetLineWidth(2)
lines[-1].SetLineColor(ROOT.kBlack)
lines[-1].Draw("SAME")

if (options.TeV == 7):
    c_single.SaveAs("idmva_nvtx_7TeV.pdf")
    c_single.SaveAs("idmva_nvtx_7TeV.root")
else:
    c_single.SaveAs("idmva_syst_10thMarch.pdf")
    c_single.SaveAs("idmva_syst_10thMarch.png")
    c_single.SaveAs("idmva_syst_10thMarch.root")
    #c_single.SaveAs("idmva_syst.root")


sys.exit()
