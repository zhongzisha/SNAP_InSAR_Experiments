import org.esa.s1tbx.insar.gpf.InSARStackOverviewNoDialog;
import org.esa.snap.core.datamodel.*;
import org.esa.snap.engine_utilities.datamodel.AbstractMetadata;
import org.esa.snap.engine_utilities.gpf.*;
import org.jlinda.core.Orbit;
import org.jlinda.core.SLCImage;

import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


/*
E:\\step1_results\\20190724.dim,E:\\step1_results\\20190817.dim,E:\\step1_results\\20191004.dim,E:\\step1_results\\20191028.dim,E:\\step1_results\\20191121.dim,E:\\step1_results\\20191215.dim,E:\\step1_results\\20200201.dim,E:\\step1_results\\20200225.dim,E:\\step1_results\\20200320.dim,E:\\step1_results\\20200413.dim,E:\\step1_results\\20200507.dim,E:\\step1_results\\20200706.dim,E:\\step1_results\\20200730.dim,E:\\step1_results\\20200823.dim,E:\\step1_results\\20201010.dim,E:\\step1_results\\20201103.dim,E:\\step1_results\\20201221.dim,E:\\step1_results\\20210114.dim,E:\\step1_results\\20210207.dim,E:\\step1_results\\20210303.dim
 */

public class DoInSARStackOverview {
    private final Map<SLCImage, File> slcFileMap = new HashMap<>(10);

    private InSARStackOverviewNoDialog.IfgStack[] findInSARProducts(final File[] inputFiles) throws Exception {

        final List<SLCImage> imgList = new ArrayList<>(inputFiles.length);
        final List<Orbit> orbList = new ArrayList<>(inputFiles.length);

        for (File file : inputFiles) {
            try {
                final Product product = CommonReaders.readProduct(file);
                final MetadataElement absRoot = AbstractMetadata.getAbstractedMetadata(product);
                final SLCImage img = new SLCImage(absRoot, product);
                final Orbit orb = new Orbit(absRoot, 3);

                slcFileMap.put(img, file);

                imgList.add(img);
                orbList.add(orb);
            } catch (IOException e) {
                throw new IOException("Error: unable to read " + file.getPath() + '\n' + e.getMessage());
            } catch (Exception e) {
                throw new Exception("Error: " + file.getPath() + '\n' + e.getMessage());
            }
        }

        try {
            final InSARStackOverviewNoDialog dataStack = new InSARStackOverviewNoDialog();
            dataStack.setInput(imgList.toArray(new SLCImage[imgList.size()]), orbList.toArray(new Orbit[orbList.size()]));

            return dataStack.getCoherenceScores();

        } catch (Throwable t) {
            return null;
        }
    }

    private Product getMasterProductByStackOverview(List<File> fileList) throws Exception {
//        final List<File> fileList = new ArrayList<>(sourceProduct.length);
//        for (Product prod : sourceProduct) {
//            final File file = prod.getFileLocation();
//            if (file != null && file.exists()) {
//                fileList.add(file);
//            }
//        }
        final File[] inputFiles = fileList.toArray(new File[fileList.size()]);

        final InSARStackOverviewNoDialog.IfgStack[] ifgStack = findInSARProducts(inputFiles);
        if (ifgStack != null) {
            final InSARStackOverviewNoDialog dataStack = new InSARStackOverviewNoDialog();
            final int masterIndex = dataStack.findOptimalMaster(ifgStack);
            final InSARStackOverviewNoDialog.IfgPair[] slaveList = ifgStack[masterIndex].getMasterSlave();
            final File mstFile = slcFileMap.get(slaveList[masterIndex].getMasterMetadata());
            return CommonReaders.readProduct(mstFile);
        }
        return null;
    }

    public static String readFileContent(String fileName) {
        File file = new File(fileName);
        BufferedReader reader = null;
        StringBuilder sbf = new StringBuilder();
        try {
            reader = new BufferedReader(new FileReader(file));
            String tempStr;
            while ((tempStr = reader.readLine()) != null) {
                sbf.append(tempStr).append(',');
            }
            reader.close();
            return sbf.toString();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (reader != null) {
                try {
                    reader.close();
                } catch (IOException e1) {
                    e1.printStackTrace();
                }
            }
        }
        return sbf.toString();
    }

    public static void main(String[] args) throws Exception {
        System.out.println("Do InSARStackOverview.");

//        for (String arg : args) {
//            System.out.println(arg);
//        }
        String content = readFileContent(args[0]);
        System.out.println(content);
        String[] filenames = content.split(",");
        final List<File> fileList = new ArrayList<>(filenames.length);
        for (String filename : filenames) {
            final File file = new File(filename);
            if (file.exists()) {
                fileList.add(file);
            }
        }

        System.out.println(fileList);

        DoInSARStackOverview obj = new DoInSARStackOverview();
        Product mstProduct = obj.getMasterProductByStackOverview(fileList);
        assert mstProduct != null;
        int width = mstProduct.getSceneRasterWidth();
        int height = mstProduct.getSceneRasterHeight();
        System.out.println(mstProduct.getName());

        FileWriter fwriter = null;
        try {
            fwriter = new FileWriter(args[1], false);
            fwriter.write(mstProduct.getName() + ',' + width + ',' + height);  // output the master date and its width and height for subset processing
        } catch (IOException ex) {
            ex.printStackTrace();
        } finally {
            try {
                assert fwriter != null;
                fwriter.flush();
                fwriter.close();
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }

    }

}
