# SNAP_InSAR_Experiments

https://forum.step.esa.int/t/how-to-setup-gpt-commandline-from-source-code/2132/6

https://www.bilibili.com/video/BV1vv411i7se

```
cd SNAP/snap-engine
mvn dependency:copy-dependencies -DoutputDirectory=../snap-engine-dependencies

cd SNAP/s1tbx
mvn dependency:copy-dependencies -DoutputDirectory=../snap-s1tbx-dependencies

Move into the directory snap-engine/snap-engine-kit and execute on the command line
mvn clean package assembly:assembly.
This will create the snap-engine-<version>.zip file.
This zip contains three directories lib, modules and licenses.
The s3tbx modules need to be added manually to the modules dir.

```

Then, the `gpt.bat` can be found in the `snap-engine-<version>.zip`.

HDF5 not found, add the `-Djava.library.path=$HDFJAVA_HOME"/lib"` to VM options.


For `DoInSARStackOverview` project,
```
Build->Edit->Artifacts->+->Jar->From modules with dependencies->Main Class->copy to the output directory and link via manifest

Add some dependencies to the Modules
```

change jblas-1.2.5 to jblas-1.2.4 is OK in CentOS 7.5 1804 64bit.
